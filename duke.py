import subprocess
import shlex
import select

from twilio.rest import Client

account = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
token = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
client = Client(account, token)

numbers = ["XXXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXX"]

legends = ["Waylon Jennings", "Willie Nelson", "George Strait", "Conway Twitty", "Johnny Cash", "Garth Brooks", "Merle Haggard"]

cmd = "tail -n 17 -f duke.log"

f = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

row = ""

while True:
    
    if p.poll(1):
        
        line = f.stdout.readline().decode("utf-8").replace("data:", "").replace("\n", "")
        row += line
        
        if line == " }":
            
            d = eval(row)

	    song = d["parameters"]["cue_title"]
	    artist = d["parameters"]["track_artist_name"]

            body = ";)\n{song}\nby {artist}\nis now playing on THE DUKE\nhttp://player.listenlive.co/29201".format(song=song, artist=artist])
            
            if artist in legends:
                
                for num in numbers:
                    
                    message = client.messages.create(to=num, from_="XXXXXXXXXXXXXXXX", body=body)
            
            row = ""
