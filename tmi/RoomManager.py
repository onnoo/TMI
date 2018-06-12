class RoomManager:
	 def __init__(self):
	 	self.room_list = {}
	 	self.current_room = 0
	 	self.ready = False

	 def loop(self):
	 	while self.ready:
	 		self.call_logic()
	 		self.call_render()
	 		self.call_input()

	 def call_logic(self):
	 	self.current_room.logic()

	 def call_render(self):
	 	self.current_room.render()

	 def call_input(self):
	 	self.current_room.get_key()

	 def add_room(self, room):
	 	if len(self.room_list) == 0:
	 		self.current_room = room
	 	elif room.name == "DefaultRoom":
	 		self.current_room = room
	 	self.room_list[room.name] = room

	 def set_room(self, room_name):
	 	self.current_room = self.room_list[room_name]

	 def start(self):
	 	self.ready = True
	 	self.loop()

	 def stop(self):
	 	self.ready = False