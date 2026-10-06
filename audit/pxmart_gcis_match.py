"""全聯門市 ↔ 經濟部商工登記分公司 嚴格比對（同縣市、一對一、不推估）"""
import re
from collections import defaultdict

FW = str.maketrans('０１２３４５６７８９－', '0123456789-')
CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
CITY_WORDS = ['台北', '新北', '桃園', '台中', '台南', '高雄', '基隆', '新竹', '苗栗', '彰化', '南投', '雲林',
              '嘉義', '屏東', '宜蘭', '花蓮', '台東', '澎湖', '金門', '連江']
OLD_COUNTY = re.compile(r'^(台北縣|台中縣|台南縣|高雄縣|桃園縣)')

def norm_city(s):
    return str(s).replace('臺', '台').strip()

def norm_name(n):
    n = norm_city(n).replace('全聯福利中心', '').replace('全聯', '').strip()
    n = re.sub(r'分公司$', '', n)
    n = re.sub(r'店$', '', n)
    n = OLD_COUNTY.sub('', n)
    for c in CITY_WORDS:
        if n.startswith(c) and len(n) > len(c):
            n = n[len(c):]
            break
    return n

def _cn_num(m):
    s = m.group(1)
    if s in CN:
        return str(CN[s])
    if s.startswith('十'):
        return str(10 + CN.get(s[1:], 0))
    return s

def norm_addr(a):
    a = norm_city(a).translate(FW)
    a = re.sub(r'^\(\d+\)', '', a)
    a = re.sub(r'[（(].*?[）)]', '', a)
    a = re.sub(r'([一二三四五六七八九十]+)段', lambda m: _cn_num(m) + '段', a)
    a = re.sub(r'(?<=[區鄉鎮市])[一-鿿]{1,3}[里村](?=[一-鿿])', '', a)
    a = a.replace('之', '-')
    m = re.search(r'(.+?[路街道](?:\d+段)?(?:\d+巷)?(?:\d+弄)?\d+(?:-\d+)?號)', a)
    return m.group(1) if m else a

def city_of(addr):
    return norm_city(addr)[:3]

def same_store_reregistrations(b, branches):
    """同名、同地址的其他登記（含已廢止）＝同一間店重新登記，開店日期取最早那筆"""
    key = (city_of(b['address']), norm_name(b['name']), norm_addr(b['address']))
    return [x for x in branches if x.get('opened_date') and
            (city_of(x['address']), norm_name(x['name']), norm_addr(x['address'])) == key]

def match_all(stores, branches):
    """stores: [{'code','name','city','address'}] -> {code: (branch, how)}"""
    by_name, by_addr = defaultdict(list), defaultdict(list)
    for b in branches:
        by_name[(city_of(b['address']), norm_name(b['name']))].append(b)
        by_addr[(city_of(b['address']), norm_addr(b['address']))].append(b)
    claimed, result = set(), {}

    def pick(cands, store_addr):
        cands = [c for c in cands if c['branch_ban'] not in claimed and c.get('opened_date')]
        if not cands:
            return None
        # 優先：登記地址與門市目前地址相同 → 核准設立 → 最新一筆
        same_addr = [c for c in cands if norm_addr(c['address']) == store_addr]
        pool = same_addr or cands
        active = [c for c in pool if c.get('status') == '核准設立']
        pool = active or pool
        return max(pool, key=lambda c: c['opened_date'])

    for how, key in (('店名', lambda s: (norm_city(s['city'])[:3], norm_name(s['name']))),
                     ('地址', lambda s: (norm_city(s['city'])[:3], norm_addr(s['address'])))):
        index = by_name if how == '店名' else by_addr
        for s in stores:
            if s['code'] in result:
                continue
            b = pick(index.get(key(s), []), norm_addr(s['address']))
            if b:
                result[s['code']] = (b, how)
                claimed.add(b['branch_ban'])
    # 第三輪：同縣市、店名結尾相同（如「草屯虎山」↔「虎山」）且唯一候選
    for s in stores:
        if s['code'] in result:
            continue
        city, sn = norm_city(s['city'])[:3], norm_name(s['name'])
        cands = [b for b in branches if city_of(b['address']) == city and b['branch_ban'] not in claimed
                 and b.get('opened_date') and b.get('status') == '核准設立'
                 and len(norm_name(b['name'])) >= 2 and sn.endswith(norm_name(b['name']))]
        if len(cands) == 1:
            result[s['code']] = (cands[0], '店名結尾')
            claimed.add(cands[0]['branch_ban'])
    # 同一間店重新登記：開店日期沿用最早的登記
    for code, (b, how) in list(result.items()):
        same = same_store_reregistrations(b, branches)
        first = min(same, key=lambda x: x['opened_date']) if same else b
        result[code] = (b, how, first)
    return result
