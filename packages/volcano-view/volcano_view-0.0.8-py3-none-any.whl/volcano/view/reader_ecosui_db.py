import codecs
import mysql.connector


# locals
from .web_exc import WebException
from .interpolator import Interpolator
from .my_tools import to_map, read_json_wx
from .period import ReportPeriod


_CFG_FILE_NAME = 'ecosui.json'


'''
    values_XX:
        value_meantype, 
        value_object_uid32, 
        value_datetime, 
        value_millisec, 
        value_quality, 
        value_value
'''

class Site:     # pylint: disable=too-few-public-methods
    def __init__(self, short_name, parent_n, sites, web_id):
        self.parent = parent_n              # указатель на родительский сайт или None для топов
        self.short_name = short_name        # Любой компонент бранша, например, "10 кВ"
        self.db_origin = None               # ???
        self.web_id = web_id                # id used when interacting with front-end
        self.full_name = parent_n.full_name + '/' + short_name if parent_n else short_name
        self.children_list = []
        self.children_map = {}              # key = short_name
        self.tags_map = {}                  # key = description(tag name), value=uid

        self.has_cumulative_data = False    # True is site has tags or its children have
        self.has_realtime_data = False      # True is site has tags or its children have

        if parent_n:
            parent_n.children_list.append(self)
            parent_n.children_map[short_name] = self
        else:
            sites.top_sites_list.append(self)
            sites.top_sites_map_short_name[short_name] = self

        sites.all_sites_list.append(self)
        sites.all_sites_map_web_id[self.web_id] = self

    def find_child(self, short_name):
        return self.children_map.get(short_name, None)


class Sites:        # pylint: disable=too-few-public-methods
    def __init__(self):
        self.top_sites_list = []
        self.top_sites_map_short_name = {}  # key = short_name
        self.all_sites_list = []
        self.all_sites_map_web_id = {}      # key = site.web_id


class EcoSUIReader:
    def __init__(self, env, log):
        self.env = env
        self.log = log
        self.qt_ = None                 # ( {id, title, eu, cumulative: bool}, ... )
        self.sites_ = None              # Sites()
        self.db_con_settings_ = None
        self.ignored_branches_ = set()  # Набор short_names, которые сразу отбрасываются

    def reload_wx(self):
        env = self.env
        
        file_name = '{}/{}'.format(env.wd, _CFG_FILE_NAME) if env.wd else _CFG_FILE_NAME
    
        data = read_json_wx(file_name)

        self.qt_ = data.get('qt', None)
        if self.qt_ is None:
            raise WebException('"qt" node not found in {}'.format(file_name))
    
        self.db_con_settings_ = data.get('connection', None)
        if self.db_con_settings_ is None:
            raise WebException('"connection" node not found in {}'.format(file_name))

        self.ignored_branches_ = set(data.get("ignore", []))
        

        # rval: ( {id, parent_id, title}, ... )
        # filter: None, '' => all
        #           'cumulative'
        #           'realtime'
    def read_hr_wx(self, f = None):

        # log = self.log
    
        try:
            if self.sites_ is None:
                self._read_config_wx()

            results = None
            if f == 'cumulative':
                results = filter(lambda x: x.has_cumulative_data, self.sites_.all_sites_list)
            elif f == 'realtime':
                results = filter(lambda x: x.has_realtime_data, self.sites_.all_sites_list)
            else:
                results = filter(lambda x: x.has_cumulative_data or x.has_realtime_data, self.sites_.all_sites_list)

            res = tuple(map(lambda x: {'id': x.web_id, 'parent_id': x.parent.web_id if x.parent else '', 'title': x.short_name}, results))
            
            return res
            
        except Exception as e:
            raise WebException(e, 500)

        # rval: ( {id, title, eu, cumulative: bool}, ... )

    def read_qt_wx(self, _cumulative: bool):
    
        # log = self.log
    
        if self.qt_ is None:
            j = read_json_wx(_CFG_FILE_NAME)
            if 'qt' not in j:
                raise WebException('"qt" node not found in {}'.format(_CFG_FILE_NAME))
            self.qt_ = j['qt']

        return self.qt_

    def read_data_wx(self, hr_ids, qt_id, all_ivl, sub_ivl, finished, setpt, dtm_to_str: bool = True, raising_sum: bool = False):
        log = self.log
        
        if self.sites_ is None:
            self._read_config_wx()

        # Qt
        qt_list = self.read_qt_wx(True)
        qt_map = to_map(qt_list, 'id')
        qt = qt_map.get(qt_id, None)
        if qt is None:
            raise WebException('Qt "{}" does not exist'.format(qt_id))

        sites = []
        for hr_id in hr_ids:
            site = self.sites_.all_sites_map_web_id.get(hr_id, None)
            if site is None:
                raise WebException('Hr "{}" does not exist'.format(hr_id))
            sites.append(site)

        # у нас setpt - в UTC. 
        crp = ReportPeriod(all_ivl, sub_ivl, finished, setpt)

        series = []

        interpol = Interpolator()
        for site in sites:
            serie = {
                'hr_id': site.web_id,
                'qt_id': qt_id,
                'values': None
            }
            tag_uid = site.tags_map.get(qt['db_path'], None)
            if tag_uid is not None:
                db_records = self._read_tag_wx(tag_uid, crp.begin(), crp.end())
                values = None
                if raising_sum:
                    values = []
                    for _i,dtm in crp.readouts():
                        values.append(interpol.try_get_value_on(db_records, dtm))
                else:
                    values = interpol.interpolate_sorted_values(db_records, crp.readouts(), crp.begin())
                    
                serie['values'] = values
                series.append(serie)
            else:
                log.debug('Serie {}/{} doesnt exist'.format(site.full_name, qt_id))

        res = {
            'cumulative': True,
            'start': crp.begin().isoformat() if dtm_to_str else crp.begin(),
            'readouts': tuple(map(lambda x: x.isoformat() if dtm_to_str else x, crp.readouts())),
            'series': series
        }
        
        log.debug(res)
        
        return res

    '''
        Сохраняет на диск txt со считанной структурой данных
    '''
    def _debug_save_struct(self):
        log = self.log

        if not self.sites_:
            log.warn('Cant export debug info: sites are not ready')
            return
            
        def __print_site(fs, s, tab):
            fs.write('{}{} [{}]\n'.format(tab, s.short_name, s.db_origin))
            for k,v in s.tags_map.items():
                fs.write('{}* {}={}\n'.format(tab, k, v))
            
            if s.children_list:
                for ss in s.children_list:
                    __print_site(fs, ss, tab + '  ')
                    
                    
        try:
            with codecs.open('debug.txt', 'w', encoding='utf-8') as f:
                for s in self.sites_.top_sites_list:
                    __print_site(f, s, '')
                    
        except Exception as ex:
            log.warn(ex)
        

    # wanted_tags_map used to filter unused tags. tag is included if wanted_tags_map[tag_name]
    def _read_config_wx(self):
        log = self.log
        
        qt_list = self.read_qt_wx(True)
        all_qt_map_by_dbpath = to_map(qt_list, 'db_path')
        cum_qt_list = tuple(filter(lambda x: x['cumulative'], qt_list))
        rtm_qt_list = tuple(filter(lambda x: not x['cumulative'], qt_list))

        self.sites_ = Sites()
        
        def __callback(cursor):
            query = ('SELECT DISTINCT object_origin FROM objects')
            cursor.execute(query, ())

            # db_origin - это путь без последнего элемента
            for db_origin, in cursor:
                names = db_origin.split('/')
                
                ignore = False
                for n in names:
                    if n in self.ignored_branches_:
                        ignore = True
                        break
                
                if ignore:
                    log.debug('Site %s ignored', db_origin)
                    continue
                
                parent_site = None
                for name in names:
                    trimmed_name = name.strip()
                    if parent_site:
                        site = parent_site.find_child(trimmed_name)
                    else:
                        site = self.sites_.top_sites_map_short_name.get(trimmed_name, None)
                    if not site:
                        site = Site(trimmed_name, parent_site, self.sites_, str(len(self.sites_.all_sites_list)))
                    parent_site = site

                parent_site.db_origin = db_origin

            # for each site get measures
            for site in self.sites_.all_sites_list:
                if site.db_origin:
                    query = ('SELECT object_uid32,object_description FROM objects WHERE object_origin=%s')
                    cursor.execute(query, (site.db_origin,))
                    ignored = []
                    for (tag_id, tag_name) in cursor:
                        if tag_name in all_qt_map_by_dbpath:
                            site.tags_map[tag_name] = tag_id
                        else:
                            ignored.append( tag_name )

                    log.debug ('{}: added {}; ignored {}'.format(site.full_name, tuple(site.tags_map.keys()), ignored))
            
        self._perform_db_operation(__callback)

        # now mark useful/unuseful
        for s in self.sites_.all_sites_list:
            for qt in cum_qt_list:
                if qt['db_path'] in s.tags_map:
                    s.has_cumulative_data = True
                    p = s.parent
                    while p and not p.has_cumulative_data:
                        p.has_cumulative_data = True
                        p = p.parent
                    break
            for qt in rtm_qt_list:
                if qt['db_path'] in s.tags_map:
                    s.has_realtime_data = True
                    p = s.parent
                    while p and not p.has_realtime_data:
                        p.has_realtime_data = True
                        p = p.parent
                    break
                    
        self._debug_save_struct()

    '''
        Считывает значения тега на указанном интервале дат
        Значения отсортированы по дате
        res: [(value, dtm), ...]
        В случае ошибки WebException
    '''
    def _read_tag_wx(self, tag_uid: int, date_start, date_end):
        assert isinstance(tag_uid, int), tag_uid

        log = self.log

        def __callback(cursor):
            rs = []
            
            # values_3, not values_03
            table_name = 'values_' + str(tag_uid % 100) if tag_uid >= 0 else 'values_' + str((-tag_uid) % 100)

            query = (
                'SELECT value_datetime, value_millisec, value_quality, value_value FROM {} WHERE value_object_uid32=%s AND value_datetime BETWEEN %s AND %s ORDER BY value_datetime ASC'.format(table_name))

            log.debug('Read {} from {} in range {}...{}'.format(tag_uid, table_name, date_start, date_end))
            cursor.execute(query, (tag_uid, date_start, date_end))

            log.debug('Parsing values...')
            for dtm, _ms, _q, v in cursor:
                # print("{},{},{},{}".format(dtm,ms,q,v))
                rs.append((v, dtm))

            log.info('Read tag<%s> on[%s .. %s]: %s values', tag_uid, date_start, date_end, len(rs))
            
            log.debug('Read: %s', rs)
            
            return rs

        return self._perform_db_operation(__callback)

    '''
        Подключается к БД и вызывает callback(cursor, args)
    '''
    def _perform_db_operation(self, callback, *args):
        log = self.log

        mysql_config = self.db_con_settings_

        con = None
        cursor = None

        try:
            log.debug('Connect to mysql {}...'.format(mysql_config['host']))
            con = mysql.connector.connect(**mysql_config)

            cursor = con.cursor()

            return callback(cursor, *args)

        except mysql.connector.Error as ex:
            raise WebException(ex)
            
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as ex:
                    log.warning(ex) # dont raise - need close connection anyway
            if con:
                try:
                    con.close()
                except Exception as ex:
                    log.warning(ex) 
