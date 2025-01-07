#ifndef LOG_H
#define LOG_H

#include <string>
#include <iostream>
#include <fstream>
#include <mutex>
#include <atomic>

extern std::ofstream log_file;
extern std::atomic<bool> DEBUG;
extern std::mutex log_mutex;

void log_message(const std::string& message) {
    std::lock_guard<std::mutex> lock(log_mutex);
    if (DEBUG.load()) {
        std::cout << message << std::endl;
    }
    if (log_file.is_open()) {
        log_file << message << std::endl;
    }
}

void set_debug_mode() {
    if (DEBUG.load()) {
        log_message("DEBUG mode enabled");
    }
}

#endif // LOG_H
