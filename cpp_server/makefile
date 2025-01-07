CXX = g++
CXXFLAGS = -std=c++17 -pthread

SRC = main.cpp config.h log.h client_handler.h dotenv.cpp
OBJ = $(SRC:.cpp=.o)

all: server

server: $(OBJ)
	$(CXX) $(OBJ) -o server

.cpp.o:
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) server
