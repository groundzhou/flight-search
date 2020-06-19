#!/usr/bin/env python3

import json
import time
import random
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=2))
s.mount('https://', HTTPAdapter(max_retries=2))


class IPBlockedException(Exception):
    pass


def get_cities():
    headers = {'Host': 'm.ctrip.com',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
               'Accept': 'application/json',
               'Accept-Language': 'zh-CN,en-US;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Content-Type': 'application/json',
               'Origin': 'https://m.ctrip.com',
               'Connection': 'keep-alive',
               'Referer': 'https://m.ctrip.com/webapp/flight/schedule/getInlandCity?&_fxpcqlniredt=09031049311771044837',
               'TE': 'Trailers'}
    url = 'https://m.ctrip.com/webapp/flight/schedule/getInlandCity?&_fxpcqlniredt=09031049311771044837'
    response = requests.get(url=url, headers=headers)
    return response.text


def get_risk():
    url1 = 'https://ic.ctrip.com/captcha/risk_inspect?callback=captcha06969497584174169&extend_param=2V6x7pDkvcrysIz84iab1iKtvBOQwgxW0uvOyJIl51OGygDNT%2BXNQDx%2Bc1jSSVBQ75PEPDipD6LFHridNBXp0OgDQxkTco8BYAKKAJWOPAo%3D&appid=100003778&business_site=search_airtickets_h5&version=2.5.33&dimensions=SzFrpP3%2BMjX%2F2sQjAuftogaUwohN16gB%2FXedHv2Ve8hP0astxUk9nSTfckdvnRB52TfKIVJjTCovfJOH66o9tvj7nKS4417F92pxkiGpnTs6H46%2Bxe7Uz6VfJcBv0q%2BAVOOtYRpDmSTGrmoCu2Fa%2BYLpNGo54Zq04GubY5Tzk62JBJ%2Bri9c831H8Nq1pjq4wDtBgOltgCYBC86%2F5J9MbMYM%2F7BYFuw4PWv1o6IwvuUHRPSih2CpD2fCrCUQI4TBQCKAw9x4TCJPqE0TKOczfwQZ5NLT5ppd0IpZBQ1akguaQaFaU4PkrP9KNBmYdaJCIcxZ1YUzPwEoaxcsNkJpNFOzTKSSnTitftADN9WFmACC5MmetB6SKllsp1%2BZHNwBDugqekcSjo63trXiR2D14Vgk%2FHwJ6%2FSRbCiNKF3JJCEMCgVmftqQjzmCqIsFN3F7p98XmhF1T6%2FkFEqNl3y5X51ytK2e672dywmLfKrqrm8EZiW9nIwCMzFASZgPD%2FTHmVcGXf%2BmBN1eO9UCqmdcGuBFdMaqTuLEskItAf3MYBgBRchJniTF5BJfxEZbs8TdkFaniv5VdVp4YWl5AR4Zx0U5kH59xJc5eOrwvTidgL5Zs%2FrGQojZBkvJai6vE9qOg&sign=a59057094c2f29091132ed81c93b13ee'
    headers = {'Host': 'ic.ctrip.com',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
               'Accept': '*/*',
               'Accept-Language': 'zh-CN,en-US;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Connection': 'keep-alive',
               'TE': 'Trailers'}
    response = requests.get(url=url1, headers=headers)
    j1 = json.loads(response.text[25: -1])
    rid = j1['result']['rid']

    url2 = 'https://ic.ctrip.com/captcha/verify_slider?callback=captcha024453110213963603&appid=100003778&business_site=search_airtickets_h5&rid=' + rid + '&version=2.5.33&verify_msg=rVL2dVimLtPZxsbywYa2ZIKEgXeJVAjKVLsVlIKdQA2LiBd33oaiZi%2BHjEYsWd51BfHrLDqf%2BVI%2FbxCrZ5gSy8PXAR5it3kXAfQrPZIDBOZs983eP%2BGDiTvg4i%2FutCZE5DFsiMQRqs4%2BvzRPc%2FFs%2FLgMWE4bh%2BS%2Fa0hko6HUECQcE2qAIRYNabDDlB%2FWa34Oamza7dClP7zXu0pA1llUDlrhIE1yPWZamDzWlnUL%2FsK3Q4lktdRotaUjCe51Vzn2hK7%2BVG4B5wSL7PEKADgI7ksMSuvegT24q7SOTTjhPomi8uzq49u%2BRJqrd9ZXItqWLEy1m7%2BGRZ4g1cLZuQ2Y%2F%2FzrDbe9%2F%2BMwLT5GrlnAK0JA19VoX%2B1ImFSLhGO8WqR0virDc1vKrmY%2FNV3P7RYaWo9V7eGp%2FrGycpyFqrw%2FKp2%2F0D7SWkvzVYoYnv%2Brgk9h%2F%2FtV%2FJYplBddha1JwBRsnTBUlTt5IasVZqP%2BaBy6v86y6epT%2BIKwO9H%2FCDH3lGrwuv6j2mgZx1sCd5kre0iGVG5%2B51obtgny7EvOyAdBu69oG3eD%2BXjkGoDHzIimqHdlnDwtAb5yfBaF3mxUYi9XdbFy%2FrWQ7gOu%2FhJXhxpILrSrRM0X%2BEOQUyTOJDG798vQpj7oC4iDITog2ySUJQALNA%3D%3D&dimensions=ZEvzrcbx4EnsTQp44p16O%2FTPzrT8duR7f2%2BcVnzWwrc8IEHI1XLgiGgwdKqZwcI%2Br2hmD3pdPjgslCEfnu3jJNboTsaCxP00%2F1MUNKDcMdzlk1UFZyEXUtfPa%2Fxmxr6L4w2Qzwl3oOnLJOTzd6dHiyKCBo3DOtCBxOj97Gx%2Bgsg6PGxk83t4LSH3slAja0SSdrxHk5nLFkPTOAPnqvSh2PYX8usT%2Bv8IuCAJCVKb9mt72jnlcKzBZmTsrjDYbbWrkwSgifGiASkFD90qEpaVDanDAvM0GJMeOHWkbSS2zfINk%2FlR81HSb%2FOgJ4UfdDZ%2BuogmdtSCIqWaxPl%2FeKpsaLuym2SnjgWyyvnyMq9cwfPVHogN5H8y2OrHaXKOdnbdzmrxhUyiot7GoUrXkNPBl%2B2I84%2BK7dt7KHQJmvgxMz0dxIiQP4jr2xzATQQOLKycStZQPE%2B7YvdMHF%2BNMz0VqYcaNpuYdV52PHXjwZyoimCAklDrjJh3ezKVJsDKXCzZVPpAGFh6fPtXvLUJamHfuY3ihsV8DIOrxje%2B4xVJdTMDIOJVmg36hluLsie%2BOsgho5UK0n9hsjOx22Io4Ia3%2BjDeCGdqVrMeDhBkAbyszXjMKgGpNIxUi9PQiKo2RNGpkvHEl%2FvhbdNLunACHaHSdh3Chr0R4AQ1FizLD1ck1ZHzv2U7DwTK%2FhKmGkzB%2BOY6iI01NJeM3Hof3HTF810ueYeFkXPKhpHfxx%2B8b6wLuFOLta70hUJsS%2FqFpxdjyYUgupx5v22NyEfVgci4qN7nHqIUUQtEhMi5BXLWL8rUTU6pSp0agQcvldBzptJLmp1P7XZfHHG5Bj1OwFtTtGgp6Nn87UzQibrKuWkPzsd8DX3qpyyCfC5M04DEc4b2jPvaWuOnTwkg7LxR395zbd%2B1usBxRqRTnHJAz2m9Ie8QVU4RnlhULACZHAy5SZhnXg7ZbWv6YZuGg3j9c8ziI%2BayNlFZ%2Flx91QvHwSs1bvLGv3ZKc2UrP08s7cM%2BSyWVWnUh&extend_param=iSGlZQho4OSS%2FKGB9EdMa9l56eWLMf22JI42bFItXwdAD1fueskfM5oFJ90ou9GbTTF%2FG6OrnXQh%2F4KUcGd1fOiepPFoeGcPRGlgeolSOIHCQeyN3QbEE1kY%2BknA4zh8INYwm3ASiHOKOrhY6Unr3JHGlxII9fpig8Rtk2qwuCEsqm6HilDGPDHYQUoz9GgkwzrIZK0mWZhnNu618D7YQw%3D%3D&sign=cdad305e9b3eff9e4c666c3c523f2c22'
    response = requests.get(url=url2, headers=headers)
    j2 = json.loads(response.text[26: -1])
    token1 = j2['result']['token']

    return rid, token1
#     url3 = 'https://ic.ctrip.com/captcha/verify_text?callback=captcha029390022785165526&appid=100003778&token=' + token1 + '&rid=' + rid + '&business_site=search_airtickets_h5&version=2.5.33&captcha_type=SELECT&verify_msg=Oa%2FES6Xi3Zh4tfD9cp9PpcNALje1OMl44vl6d4CrCYguA2eYy0Q1DtjukCCrScYjL3df7IL4R4it0qPyuVTatnaDGoKepP8AE7ZR%2ByPmF36M2z%2Ffc9pqeUZ2NFDFEKxc%2B8uGeTGMW7FClTlGaK4HTINTJ88CuNH7TJ7VyuNuWmbZpX5nXpGMlP%2FSfXbXLdLWTROZ8BCRvwplHncCr8EMVZVKJLF8SllPgK%2BioQDj%2FpepY5JL9St2LNTzGE1korvdMwsdIqRfIyd7pxnryOx67Uj2h%2FoJK3AHUs2zV%2FcJ6C%2FshLL4MEKkLuMe1tL3Bd%2BAdkSGftxydz9%2FjUycvB4kWk4lHWdFLqlzD%2FFsLX15F1RhAbjRwlAjUTAmJ1XZJIfE7Ke28TA7qyfQpQLRyveA98LjvFufgHchH01au5fbGkEMdwfxKmYsg726n6wzwg6MbYdFYpSgl62WLwX%2BTvv0cY7OjDLrYMWiD3jk%2F9SNvLw5O8vzWOfL5DIJpBuoro3%2F2JnloomAEZDkP7%2BGahERTS1HrpLmw495h7Zr6Mf%2BmzGr3uDOEchhf0Z%2FcAjGoaqNGVJGolYTzz2grlwj1hOWr9SOJokPEy9zBz3glDT4dJzm%2B752erSWlIQcyqjamQ%2BFI0ri0QemlwBaebX3w4Obw3N69kfOTYE4%2Bl2NmgCMUMWr83U81Ohh9Kuvr0Aj40i3X%2FqYo62ukUR2vcO8VwKQ5uAWjc%2FbZks61TbBJKYgCk8s88tm87ovZfyNrfOkwLoyc2cCg74sajOlTcIp8OGZ%2F95LqIyC6vo8Dd7B2h9Mg%2FsvMZNSC74g%2B9bSvSmrnJXp%2Fnw86l1MGu0D5wlRX2cjGDJxjVmdb45tAacxrdhkhkRso2PhMV6U02i2%2Bc0Kai94O8ROznlAVDrmzKWTimgoP5Mbo4I%2Bg6uFGg9l%2B4M00r6rKDmDy4J7yjDS76G85y99mCgzli51bqPBtMYS3F9ouyUA6DWy77sL45pz2SZXeIwJARrqU9kyn%2F1wE7WNO9bFt4x%2BlP5uG6reHxMS%2FPCdP30I7cFi7B6nsPo5d53QaXAiS4G9jY2nT1Cce3DCzkjq97rlk0JOOHXxcZUCYPjMBZn22I9Z3oU03g6s1dWhlBYgmDEehHcQCpQPSC7Hi%2BAQzGjBfo9bQPhVUxy5ODI5yOxODaevjnJ5QKigVioP913kFyCA0H%2BROr2y9Gr046mtS2zCohkhmuyYz41yR5wIAze5DM26Eu%2FdZOxymiLUuuuXyPxANaxV%2BQucGfMvSQv%2FHRgrdH1GhA%2Bh2tl0u695ZYWuE6Dr%2F%2FwaxzArh0WneTsIcdjsIPnTMgmqxCXIp3W3xLa7n2H5zb3CWYVQC6PWmArO%2FtP4GlPse0DosVmuROKj7xdtymjQbrF4aQcH%2FWocF%2FIF019z3rZ2kK6tHZ20WpGcGre6s2QNPSMwuhI9FwyhajVPWk4vEjVtNSVPLiw3ots5%2BNDrTbsMdmKH1q7J0O9TneWphIFbymsCU3nqKTcTjb%2FjWDXlkjtYXYi4NShHcTG9tyypwTci5DJF8picSIYaUvzX0hLFO49b1wqTw8kUMS6UUK0YRw0lyZZoNMlRDgXfEmq8Qr6wZE%2FhFRTouPoagQLKzkpgh2zAGW2QjiOWnHisA4EagvFPxsv0ZEiZLWQAHDTJu6Hx%2F%2FpIHhPgTPkFOCXZqqBiyIxf8%2BNQbn29Y17XYAdZupBhZoxNGYlvt7tVULTPAPBY2%2BmWf95pymvcwKez8xPO%2B2Rn%2BIsD129xSWOtMO5sB%2FHpi3J74ybB14I3j%2FE%2BbYVXWxG0sXWTznPln43MvF9B%2Bxg8rE%2FlKSjFrJdG6q0FiUlQr9%2BxyMNtncT21wl1tKEobwHjQyoHPOQlDjSPwDrBSRnPS4hzTjgVb0IJVNDniOY9PkK1yXNDkW%2FarcC8vTNVPxBbKOjA1t49HSGRSve1H%2FibvVX1TDLPzWCfJ1Szb9PghK7oWurXRZQXsWEwLGbAwYo7yNR18ftA%2Fsw1XSTj4XSTXrl6Zah0HxluxYeOGSotWilLOE9mYDy8RdvHdm4AHhwwLstaYIa0Y0L8lJepWMQYwzE%2B27wgJ15GkiwONicmmCQ3xR7LoFZL%2BqLERY8KyDOEaaI%2FxALh0Z8fIQlEgVno6AiW%2Faa8tlfqf2a50VmoeR1CBWHd7kG1p9hXIJhjyAit%2FwGdnuZN%2FfpTLw%2FvTSm26D1ZJw%2B9GsKPW6rJsHHSxU4dlgmFTF4oSCG2jQ9PpWMZEqFk1ZREMjL7Aae8gZK7t%2FHv6XzZAliiQbcX2Aie5ZYE5QmCcMjVYpY3YwIVCLKBTqNzfNDtvivk00JovRZiYb53tK5uxXZnBx7TEwg%2BNRDNvBb2nShPndU67t9%2F64%2BSYjMLBSpFRxxZuJxkFN1w6kJ4zHe%2Br6fz2gvOlGuU31%2BlcB9RbXcwjqRUy2i8MqpADPq9Xcfgo7C3a%2FUjWsuJKcb3N6wKs9zZh2%2F1%2BZIWeEuy29p6GpuJP5XW%2FBkeqOUasy%2BMtcM%2Bib8czq4jV5JVErshmMEJBJbBM7qpMvpPqPkTp62gJaEzdoRptZRQG%2FKWW3Ze53rEqQXkBPYUv3VQZPyVd7jS0r8%2BDu%2BTHFcNfoxU441Ank3wNcYdNAGHQ1Deuu%2BK3eECncyVGTybUcfiF6yxlwhfM6ohpVOnHTnpWqojlMC5JTdc0omlWdBsZaop62gmQ3xuj8Ap6rmPT6ytcvGxA1II2ljJp2OALq1vHYLJ0w2N%2Fr76GAtnlJ4otELj4skfpRycGnjC7WUKctnD%2BqpPT%2FpYIkdUmNf8n585PKyiwJKxcS0I%2FQFMF32ZgR%2FfxMVwbpb4BKaJrNdMSLSMxQb318eaeEfXznKql6i42ljjxw2QoMA21x%2Bfc1bxCaNpCD1PbhUJ87pmV%2BIMclEngnbm8xecBhc8hOkZu0rwx9A3TOkpCMEfonwxk11GCO%2BfRN8O%2BsFtOKa8bfAW2KVky2mCGy4EEvyKY%2FWgBtVv%2B2KxmBoINiliNUuKHdlfBjf82bn7f05PTpD5eDguVkhRMecI2tu7qcvoJVHjfFZziuV2hUT1T713kCuTTHBDcHLARtzLZbma88TIbV7cZ7nXgVWnZLUoHjQuVWn2RVIItzsIqYB6dMYUCdVGd%2B9bpHtF%2F9NrLuF8GdT%2FSe98mVY%2Fsby1%2F1iIQZMVqqgXmMBq63uGFQHf32DRxbKluKSj5AbPZERIEEJNpISkjDDMBrey8GOuvzH9YueLoJsv9BjGJO6DKI7us6q4qFQep91%2BYisUK3R4axqyyJD3gQIkp%2Bg5Q4dGhxPn5TM9PLKBSLGNMovwyc9yFNpGhtPnKAyxlxZJCX6HjurD2JpDlknsyUJBQYOlbhXkRxPknkyVq8DJGdRGECjyL9J5NIIefNiOuKqdQTNIuZuwOM6Z97ZvHtDDSaDdPmPz2cRCiwPT2PfXek%2FYCrcEjaoE8KV%2F%2FIeyBilxJVIjdQqbo4qtNBmMGVoQzENE40KEXh%2BibRGZVZUS019L4cTBUJhQooqk6WFuh9jWoXv6fRQsqnpALMiJL50aKfs5VkqUbNLjUU2U9WkOrmgAA97z&dimensions=SzFrpP3%2BMjX%2F2sQjAuftogaUwohN16gB%2FXedHv2Ve8hP0astxUk9nSTfckdvnRB52TfKIVJjTCovfJOH66o9tvj7nKS4417F92pxkiGpnTs6H46%2Bxe7Uz6VfJcBv0q%2BAVOOtYRpDmSTGrmoCu2Fa%2BYLpNGo54Zq04GubY5Tzk62JBJ%2Bri9c831H8Nq1pjq4wDtBgOltgCYBC86%2F5J9MbMYM%2F7BYFuw4PWv1o6IwvuUHRPSih2CpD2fCrCUQI4TBQCKAw9x4TCJPqE0TKOczfwQZ5NLT5ppd0IpZBQ1akguaQaFaU4PkrP9KNBmYdaJCIcxZ1YUzPwEoaxcsNkJpNFOzTKSSnTitftADN9WFmACC5MmetB6SKllsp1%2BZHNwBDugqekcSjo63trXiR2D14VheDZyJQvJr4rTbIBGou4c%2B2kaKmzQaKLNQM0eBk9808ahsu1DMtOx7vghIox8g8tHFXEVMVWCa0JOTl6UDKhQV31DUoEeoBNuw4M12J2UhypJ0%2B%2BqBTCZF36oFyi%2FImPOrdtYJZFvgkWRaguz8tiT19ItmPLA8mnRlbNhlJ2vDOa6c55AvF%2FXw1X072Rv7nAwVMxXj5XLaPYwrXNpQbZKVKDGJoC1NnafHB2tuHdbFu&extend_param=iSGlZQho4OSS%2FKGB9EdMa9l56eWLMf22JI42bFItXwdAD1fueskfM5oFJ90ou9GbTTF%2FG6OrnXQh%2F4KUcGd1fOiepPFoeGcPRGlgeolSOIHCQeyN3QbEE1kY%2BknA4zh8INYwm3ASiHOKOrhY6Unr3JHGlxII9fpig8Rtk2qwuCEsqm6HilDGPDHYQUoz9GgkwzrIZK0mWZhnNu618D7YQw%3D%3D&sign=abc1f90165c4504227737023cf9f11cf'
#     response = requests.get(url=url3, headers=headers)
#     j3 = json.loads(response.text[26: -1])
#     print(j3)
#     token2 = j3['result']['token']
#
#      print(rid, token1, token2)


def request(source, destination, date, rid, token):
    url = 'https://m.ctrip.com/restapi/soa2/14022/flightListSearch?_fxpcqlniredt=09031124412121055112'
    j = {"contentType": "json", "flag": 8,
         "head": {"auth": None, "cid": "09031124412121055112", "ctok": "", "cver": "1.0",
                  "extension": [{"name": "appId", "value": "100008344"}, {"name": "aid", "value": "66672"},
                                {"name": "sid", "value": "508668"}, {"name": "protocal", "value": "https"}],
                  "lang": "01", "sid": "8888", "syscode": "09"}, "preprdid": "",
         "rid": rid, "rtoken": token,
         "searchitem": [{"accode": destination, "dccode": source, "dtime": date}], "subchannel": None,
         "tid": "{d03ed6d8-24f3-4eab-b26e-2d49ddb865fc}", "trptpe": 1}
    headers = {'Host': 'm.ctrip.com',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
               'Accept': 'application/json',
               'Accept-Language': 'zh-CN,en-US;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/json',
               'Origin': 'https://m.ctrip.com',
               'Connection': 'keep-alive',
               'Referer': 'https://m.ctrip.com/html5/flight/swift/domestic/' + source + '/' + destination + '/' + date,
               'TE': 'Trailers'}

    try:
        response = s.post(url=url, headers=headers, json=j, timeout=3)
        fltitem = json.loads(response.text).get('fltitem', None)
        flights = []
        if fltitem:
            for f in fltitem:
                if len(f['mutilstn']) == 2:
                    continue

                punctuality = [i['stip'] for i in f['mutilstn'][0]['comlist'] if i['type'] == 2]
                line = [f['mutilstn'][0]['dportinfo']['aport'],
                        f['mutilstn'][0]['dportinfo']['aportsname'],
                        f['mutilstn'][0]['dportinfo']['bsname'],
                        f['mutilstn'][0]['dportinfo']['city'],
                        f['mutilstn'][0]['dportinfo']['cityname'],
                        f['mutilstn'][0]['aportinfo']['aport'],
                        f['mutilstn'][0]['aportinfo']['aportsname'],
                        f['mutilstn'][0]['aportinfo']['bsname'],
                        f['mutilstn'][0]['aportinfo']['city'],
                        f['mutilstn'][0]['aportinfo']['cityname'],
                        f['mutilstn'][0]['basinfo']['aircode'],
                        f['mutilstn'][0]['basinfo']['airsname'],
                        f['mutilstn'][0]['basinfo']['flgno'],
                        f['mutilstn'][0]['craftinfo']['craft'],
                        f['mutilstn'][0]['craftinfo']['kind'],
                        f['mutilstn'][0]['craftinfo']['cname'],
                        f['mutilstn'][0]['dateinfo']['ddate'],
                        f['mutilstn'][0]['dateinfo']['adate'],
                        f['policyinfo'][0]['priceinfo'][0]['price'],
                        f['policyinfo'][0]['priceinfo'][0]['drate'],
                        f['policyinfo'][0]['classinfor'][0]['display'],
                        punctuality[0] if punctuality else '',
                        len(f['mutilstn'][0]['fsitem'])]
                flights.append(','.join([str(i) for i in line]) + '\n')
    except requests.exceptions.RequestException as e:
        print('Time out')
        raise Exception("Time out")
    except KeyError as e:
        raise Exception("Key Error")
    except:
        raise Exception("Other error")
    else:
        rlt = json.loads(response.text).get('rlt', None)
        if rlt == 508 or rlt == 509:
            raise IPBlockedException
        elif rlt != 0:
            raise Exception('No flight')
        return flights


def main():
    # get_risk()
    # with open('../data/flights.csv', 'a') as f:
    #     f.writelines(request('ZUH', 'CKG', '2020-06-20'))
    # 日期列表
    date_list = [datetime.strftime(datetime.strptime('2020-06-19', '%Y-%m-%d') + timedelta(i), '%Y-%m-%d')
                 for i in range(365)]

    # 城市列表
    with open('../data/cities.json') as f:
        cities = json.load(f)['inLandData']['inlandCity']
        city_codes = list(set([c['code'] for c in cities]))
        city_codes.sort()

    # 循环爬取
    exception = 0
    i = 0
    j = 173
    rid, token = "BBE0515DAAFC4CB09A66E7C70B095E6F", "p0a7d551282e59075325029534b6fbdbd8326e82cfbee"
    for d in date_list:
        while i < len(city_codes):
            while j < len(city_codes):
                if city_codes[i] != city_codes[j]:
                    try:
                        flights = request(city_codes[i], city_codes[j], d, rid, token)
                        # 写入文件
                        with open('../data/flights.csv', 'a') as f:
                            f.writelines(flights)
                    except IPBlockedException:
                        exception += 1
                        print('IP blocked', i, city_codes[i], j, city_codes[j], d)
                        time.sleep(5)
                    except:
                        exception += 1
                        print('Error', i, city_codes[i], j, city_codes[j], d)
                        time.sleep(5)
                    else:
                        exception = 0
                if exception == 5:
                    break
                j += 1

            if exception == 5:
                break
            j = 0
            i += 1

        if exception == 5:
            break
        i = 0


if __name__ == '__main__':
    main()
