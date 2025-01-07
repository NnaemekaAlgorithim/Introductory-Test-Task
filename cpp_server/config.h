#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <cstdlib>
#include <iostream>
#include "dotenv.h"

extern int PORT;
extern int BUFFER_SIZE;
extern bool DEBUG;
extern std::string FILE_PATH;

void load_config() {
    // Load environment variables
    dotenv::load();

    // Retrieve and convert values
    PORT = std::stoi(dotenv::get("PORT", "44445"));
    BUFFER_SIZE = std::stoi(dotenv::get("BUFFER_SIZE", "1024"));
    DEBUG = dotenv::get("DEBUG", "false") == "true";
    FILE_PATH = dotenv::get("FILE_PATH", "/path/to/your/file.txt");
}

std::string get_file_path() {
    return FILE_PATH;
}

#endif // CONFIG_H
