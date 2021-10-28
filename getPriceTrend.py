from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from replit import db

def getPriceTrend(build):

	time = []
	eth = []
	usd = []
	
	for item in db["prices"][build]:
			
			time.append(datetime.strptime(item[0],"%m/%d/%Y, %H:%M:%S") + timedelta(hours=8))
			eth.append(item[1])
			usd.append(item[2])
	
	
	fig,ax = plt.subplots()
	ax.plot(time,eth,color="red",marker="o")
	ax.set_xlabel("Time",fontsize=10)
	ax.tick_params(labelrotation=45)
	ax.set_ylabel("ETH",color="red")
	
	ax2=ax.twinx()
	ax2.plot(time,usd,color="blue",marker="o")
	ax2.set_ylabel("USD",color="blue")
	
	plt.title(build + " build")
	plt.savefig(build+".png")

	return