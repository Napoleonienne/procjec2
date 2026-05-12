#pragma once

#include <cmath>
#include <string>

struct Vec2 {
    float x{0.0f};
    float y{0.0f};

    constexpr Vec2() = default;
    constexpr Vec2(float x_val, float y_val) : x(x_val), y(y_val) {}

    constexpr Vec2 operator+(const Vec2& other) const {
        return Vec2{x + other.x, y + other.y};
    }

    constexpr Vec2 operator-(const Vec2& other) const {
        return Vec2{x - other.x, y - other.y};
    }

    constexpr Vec2 operator*(float other) const {
        return Vec2{x * other, y * other};
    }

    constexpr Vec2 operator/(float other) const {
        return Vec2{x / other, y / other};
    }
};

inline std::string to_string(const Vec2& vec) {
    return "(" + std::to_string(vec.x) + "," + std::to_string(vec.y) + ")";
}

inline float norme(const Vec2& vec) {
    return std::sqrt(vec.x * vec.x + vec.y * vec.y);
}

inline Vec2 normalize(const Vec2& vec) {
    const float n = norme(vec);
    return n == 0.0f ? Vec2{} : vec / n;
}

inline float dot(const Vec2& vec_a, const Vec2& vec_b) {
    return vec_a.x * vec_b.x + vec_a.y * vec_b.y;
}

inline float cross(const Vec2& vec_a, const Vec2& vec_b) {
    return vec_a.x * vec_b.y - vec_a.y * vec_b.x;
}

inline Vec2 rotate(const Vec2& vec, float angle) {
    constexpr float pi = 3.14159265358979323846f;
    const float rad = pi * angle / 180.0f;
    const float cos_a = std::cos(rad);
    const float sin_a = std::sin(rad);
    return Vec2{vec.x * cos_a - vec.y * sin_a, vec.x * sin_a + vec.y * cos_a};
}
