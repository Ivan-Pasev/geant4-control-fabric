#pragma once
#include <cstdlib>
#include <stdexcept>
#include <string>

namespace g4cf {
inline std::string env(const char* key, const std::string& fallback = {}) {
  if (const char* v = std::getenv(key)) return v;
  return fallback;
}
inline int env_int(const char* key, int fallback) {
  const auto v = env(key);
  return v.empty() ? fallback : std::stoi(v);
}
inline long env_long(const char* key, long fallback) {
  const auto v = env(key);
  return v.empty() ? fallback : std::stol(v);
}
inline double env_double(const char* key, double fallback) {
  const auto v = env(key);
  return v.empty() ? fallback : std::stod(v);
}
inline bool env_bool(const char* key, bool fallback) {
  const auto v = env(key);
  if (v.empty()) return fallback;
  if (v == "1" || v == "true" || v == "TRUE" || v == "on" || v == "ON") return true;
  if (v == "0" || v == "false" || v == "FALSE" || v == "off" || v == "OFF") return false;
  throw std::runtime_error(std::string("Invalid boolean environment value for ") + key + ": " + v);
}
}
