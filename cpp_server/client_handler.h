#ifndef CLIENT_HANDLER_H
#define CLIENT_HANDLER_H

#include <iostream>
#include <fstream>
#include <cstring>
#include <thread>
#include <netinet/in.h>
#include <unistd.h>
#include "log.h"
#include "config.h"

void handle_client(int client_socket, sockaddr_in client_address, const std::string& file_path) {
    char buffer[BUFFER_SIZE];
    std::string client_ip = inet_ntoa(client_address.sin_addr);
    int client_port = ntohs(client_address.sin_port);

    log_message("Connection established with " + client_ip + ":" + std::to_string(client_port));

    while (true) {
        memset(buffer, 0, BUFFER_SIZE);
        ssize_t bytes_received = recv(client_socket, buffer, BUFFER_SIZE - 1, 0);
        if (bytes_received <= 0) {
            break;
        }

        std::string message(buffer);
        message = message.substr(0, bytes_received);
        log_message("Received from " + client_ip + ":" + std::to_string(client_port) + ": " + message);

        try {
            bool found = search_file(file_path, message);
            std::string response = found ? "STRING EXISTS\n" : "STRING DOES NOT EXIST\n";
            send(client_socket, response.c_str(), response.size(), 0);
        } catch (const std::exception& e) {
            std::string error_response = "Error: " + std::string(e.what()) + "\n";
            send(client_socket, error_response.c_str(), error_response.size(), 0);
            log_message("Error while handling client request: " + std::string(e.what()));
        }
    }

    close(client_socket);
    log_message("Connection closed with " + client_ip + ":" + std::to_string(client_port));
}

bool search_file(const std::string& file_path, const std::string& data) {
    std::ifstream file(file_path);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open data file: " + file_path);
    }

    std::string line;
    std::string trimmed_data = trim(data);
    while (std::getline(file, line)) {
        if (trim(line) == trimmed_data) {
            return true;
        }
    }

    return false;
}

#endif // CLIENT_HANDLER_H
