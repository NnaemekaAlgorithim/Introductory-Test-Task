#include "dotenv.h"
#include <fstream>
#include <sstream>

namespace dotenv {

void load() {
    std::ifstream file(".env");
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            if (line.empty() || line[0] == '#') continue; // Skip comments and empty lines
            size_t delimiter_pos = line.find('=');
            if (delimiter_pos != std::string::npos) {
                std::string key = line.substr(0, delimiter_pos);
                std::string value = line.substr(delimiter_pos + 1);
                std::setenv(key.c_str(), value.c_str(), 1);
            }
        }
    }
}

std::string get(const std::string& key, const std::string& default_value) {
    const char* value = std::getenv(key.c_str());
    return value ? value : default_value;
}

} // namespace dotenv
