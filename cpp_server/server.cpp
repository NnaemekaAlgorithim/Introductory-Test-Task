#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <vector>
#include <atomic>
#include <cstdlib>
#include "config.h"
#include "log.h"
#include "client_handler.h"

std::vector<std::thread> threads;    // Store threads for client handling
std::ofstream log_file;              // Log file stream

int main() {
    // Load configuration from .env file
    load_config();

    // Open log file
    log_file.open("server.log", std::ios::app);
    if (!log_file.is_open()) {
        std::cerr << "Failed to open log file" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Set DEBUG mode
    set_debug_mode();

    // Get the file path from the configuration
    std::string file_path = get_file_path();

    try {
        start_server(file_path);
    } catch (const std::exception& e) {
        std::cerr << "Server error: " << e.what() << std::endl;
        log_message("Server error: " + std::string(e.what()));
    }

    // Join threads before exiting
    for (auto& t : threads) {
        if (t.joinable()) {
            t.join();
        }
    }

    // Close the log file
    if (log_file.is_open()) {
        log_file.close();
    }

    return 0;
}
