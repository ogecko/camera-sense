check:
    # Every 8 seconds for 1 minute
	python3 capture.py -d ./data/pizza -f check -t 1 -i 0.13
starter:
    # Every minute for 2 hour
	python3 capture.py -d ./data/pizza -f starter -t 120 -i 1
proof:
    # Every minute for 4 hour
	python3 capture.py -d ./data/pizza -f proof -t 240 -i 1
stirfry:
    # Every minute for 4 hour
	python3 capture.py -d ./data/pizza -f stirfry -t 240 -i 0.25
april:
	python3 april.py
stop: 
	pkill -f /usr/bin/python3
dev-server: 
	cd api; ~/.local/bin/fastapi dev server.py 
dev-client: 
	cd app; yarn run dev 
build-client: 
	cd app; yarn run build 
run-server: 
	cd api; ~/.local/bin/fastapi run server.py 
web: 
	cd dist/spa; python3 -m http.server 9010 

