import os, json, time, requests, hashlib
from pathlib import Path
import pandas as pd 

# Location of Json files
PATHS = './Archive'
pathdown = 'test'
# Loading and saving the risk-level data
def loading_new():
    # Parms from Ajax.js
    key = '3C502C97ABDA40D0A60FBEE50FAAD1DA'
    timestamp = str(int(time.time()))
    token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
    nonce = '123456789abcdefg'
    passid = 'zdww'
    temp = timestamp + token + nonce + timestamp
    temp = temp.encode('utf-8')
    signatureHeader = hashlib.sha256(temp).hexdigest().upper()
    temp = timestamp + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + 'QkjjtiLM2dCratiA' + timestamp
    temp = temp.encode('utf-8')
    zdwwsignature = hashlib.sha256(temp).hexdigest().upper()
    
    # Send post requests
    url = 'http://103.66.32.242:8005/zwfwMovePortal/interface/interfaceJson'
    data = {"appId":"NcApplication",
            "paasHeader":passid,
            "timestampHeader":timestamp,
            "nonceHeader":nonce,
            "signatureHeader":signatureHeader,
            "key":key}
    header = {"x-wif-nonce": "QkjjtiLM2dCratiA",
              "x-wif-paasid": "smt-application",
              "x-wif-signature": zdwwsignature,
              "x-wif-timestamp": timestamp,
              "Origin": "http://bmfw.www.gov.cn",
              "Referer": "http://bmfw.www.gov.cn/yqfxdjcx/risk.html",
              "Content-Type": "application/json; charset=UTF-8"}
    r = requests.post(url, data = json.dumps(data), headers=header)
    
    # Save Json file
    path_json = PATHS
    global pathdown
    pathdown = path_json+'/'+r.json()['data']['end_update_time']+'.js'
    with open(pathdown, 'w', encoding="utf8") as outfile:
        json.dump(r.json(), outfile, ensure_ascii=False)

# Removing duplications
def dup(risk1, risk2):
    # Check if there is any empty area
    if len(risk1)==0:
        shift = pd.DataFrame(risk2).explode('communitys').drop_duplicates()
        shift['_merge'] = 'right_only'
        return(shift)
    elif len(risk2)==0:
        shift = pd.DataFrame(risk1).explode('communitys').drop_duplicates()
        shift['_merge'] = 'left_only'
        return(shift)
    else:     
        df1 = pd.DataFrame(risk1).explode('communitys').drop_duplicates()
        df2 = pd.DataFrame(risk2).explode('communitys').drop_duplicates()
    
    # Compare df1-the previous one with df2-the newer one
    df = df1.merge(df2, indicator=True, how='outer')
    # left_only might be item that has been removed
    # right_only might be item that was updated
    shift = df.loc[df['_merge']!='both',:]
    return(shift)    
    
# Comparison with fomer one
def check():
    high_flag = 1
    middle_flag = 1
    entries = Path(PATHS)
    f = open(pathdown, encoding="utf8")
    json1 = json.load(f)
    f.close()
    risk1 = json1['data']['highlist']
    risk2 = json1['data']['middlelist']
    df1 = pd.DataFrame(risk1).explode('communitys').drop_duplicates()
    df2 = pd.DataFrame(risk2).explode('communitys').drop_duplicates()
    shift1 = df1.loc[:]
    shift2 = df2.loc[:]
    shift1['level'] = "high"
    shift2['level'] = "middle"

    shift = shift1.merge(shift2, indicator=False, how='outer')

    if len(shift) > 0:
        shift.drop(['type', 'area_name'], axis=1, inplace=True)
        shift.to_csv(PATHS + '/' + json1['data']['end_update_time'] + '.csv', encoding='utf_8_sig')
    else:
        text_file = open(PATHS+'/'+json1['data']['end_update_time']+".txt", "w")
        n = text_file.write('No updated')
        text_file.close()


def comparsion():
    high_flag = 1
    middle_flag = 1
    entries = Path(PATHS)
    files = sorted(entries.glob("*.js"), key=os.path.getmtime, reverse=True)
    f = open(files[1], encoding="utf8")
    json1 = json.load(f)
    f.close()
    f = open(files[0], encoding="utf8")
    json2 = json.load(f)
    f.close()
    # High-risk
    risk1 = json1['data']['highlist']
    risk2 = json2['data']['highlist']
    # Removing duplications
    if len(risk1)==len(risk2)==0:
        high_flag = 0
    else:
        shift1 = dup(risk1, risk2)
        shift1['level'] = "high"
    
    # Mid-risk
    risk1 = json1['data']['middlelist']
    risk2 = json2['data']['middlelist']
    # Removing duplications
    if len(risk1)==len(risk2)==0:
        middle_flag = 0
    else:
        shift2 = dup(risk1, risk2)
        shift2['level'] = "middle"
    
    # Merge

    if high_flag==middle_flag==0:
        shift = pd.DataFrame()
    elif high_flag==0:
        shift = shift2
    elif middle_flag==0:
        shift = shift1
    else:
        shift = shift1.merge(shift2, indicator=False, how='outer')

    shift['_merge'] = shift['_merge'].astype(str)    
    shift.loc[shift['_merge']=='left_only', '_merge'] = 'removed'
    shift.loc[shift['_merge']=='right_only', '_merge'] = 'new'
    shift['date'] = json2['data']['end_update_time'][0:10]
    
    if len(shift)>0:
        shift.drop(['type', 'area_name'], axis=1, inplace=True)
        shift.to_csv(PATHS+'/'+json2['data']['end_update_time']+'.csv', encoding='utf_8_sig')
    else:
        text_file = open(PATHS+'/'+json2['data']['end_update_time']+".txt", "w")
        n = text_file.write('No updated')
        text_file.close()
if __name__ == '__main__':
    loading_new()
    check()
    #comparsion()
    if os.path.exists(pathdown):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(pathdown)
        # os.unlink(path)
    else:
        print('no such file:%s' % my_file)  # 则返回文件不存在