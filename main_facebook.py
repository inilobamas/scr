# # -*- coding: utf-8 -*-
# """
# Created on Sat Jul 30 03:26:04 2016
# Facebook Crawler
# License to @author: Taufik Sutanto
# https://tau-data.id
# """
# import facebook, sys, requests
# access_token = ‘Copas yang dari FAB API Explorer tadi Gan ke sini’ # https://developers.facebook.com/tools/explorer/
# pages = [‘me’, ‘sutanto.org’,‘ElasticSearch.Indonesia’,‘Kirana.Edukasi.Indonesia’] #  Tambahkan Pages lain sebanyak hasrat Agan .. 🙂
# filename = ‘Facebook_Posts.txt’ # Ini nama file untuk menyimpan Posts-nya
# Post_Limit = 100 # limit banyaknya post tiap page, kalau mau unlimited ganti dengan float(‘Inf’)
# def getLikes(pos):
#     “”” Warning, Fungsi ini sangat lambat utk posts yang likesnya banyak,
#         Fungsi ini sekedar menjelaskan bagaimana paging di sub keys request result
#     “””
#     N = 0
#     while True:
#         try:
#             pos = requests.get(pos[‘paging’][‘next’]).json()
#             N+=len(pos[‘data’])
#         except:
#             break
#     return N
# if __name__ == “__main__”:
#     graph = facebook.GraphAPI(access_token)
#     file = open(filename,‘w’)
#     for page in pages:
#         print(‘\nAccessing Page: %s’ %page, flush=True)
#         posts = graph.get_connections(id=page, connection_name=‘feed’) #posts
#         count=0; loop=True
#         while loop:
#             try:
#                 for results in posts[‘data’]:
#                     sys.stdout.write(“\r”);sys.stdout.write(“%d posts” %(count+1));sys.stdout.flush()
#                     dTxt=‘{username:”‘+results[‘from’][‘name’]+‘”, ‘
#                     dTxt+=‘date:’+results[‘created_time’]+‘, ‘
#                     try:
#                         Nlikes = len(results[‘likes’][‘data’])
#                         if Nlikes>=25:
#                             Nlikes += getLikes(results[‘likes’])
#                         dTxt+=‘likes:’+str(Nlikes)+‘, ‘
#                     except:
#                         dTxt+=‘likes:0, ‘
#                     try:
#                         dTxt+=‘message:”‘+results[‘message’]+‘”}’
#                     except:
#                         dTxt+=‘message:”-“}’
#                     file.write(str(dTxt.encode(‘utf8’, errors=‘ignore’))[2:]+‘\n’)
#                     count+=1
#                     if count>=Post_Limit:
#                         loop=False; break
#                 posts = requests.get(posts[‘paging’][‘next’]).json()
#             except:
#                 break
#     file.close()