#include "FlowSensor.h"

void FlowSensor_Init(FlowSensor *fs, uint16_t type, GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin) {
    fs->pulse_per_liter = type;
    fs->pulse = 0;
    fs->total_pulse = 0;
    fs->last_time_ms = HAL_GetTick();
    fs->flow_rate_s = 0;
    fs->flow_rate_m = 0;
    fs->flow_rate_h = 0;
    fs->volume = 0;
    fs->GPIOx = GPIOx;
    fs->GPIO_Pin = GPIO_Pin;

    // GPIO must be initialized beforehand in CubeMX (Input with EXTI interrupt)
}

/**
 * @brief ISR callback (call from EXTI IRQHandler)
 */
void FlowSensor_Count(FlowSensor *fs) {
    fs->pulse++;
}

void FlowSensor_Read(FlowSensor *fs, int32_t calibration) {
    uint32_t now = HAL_GetTick(); // ms
    uint32_t dt = now - fs->last_time_ms;
    if (dt == 0) return;

    float liters_per_pulse = 1.0f / (fs->pulse_per_liter + calibration);

    fs->flow_rate_s = (fs->pulse * liters_per_pulse) / ((float)dt / 1000.0f);
    fs->volume += fs->pulse * liters_per_pulse;
    fs->total_pulse += fs->pulse;

    fs->pulse = 0;
    fs->last_time_ms = now;
}

uint32_t FlowSensor_GetPulse(FlowSensor *fs) {
    return fs->total_pulse;
}

float FlowSensor_GetFlowRate_h(FlowSensor *fs) {
    fs->flow_rate_h = fs->flow_rate_s * 3600.0f;
    return fs->flow_rate_h;
}

float FlowSensor_GetFlowRate_m(FlowSensor *fs) {
    fs->flow_rate_m = fs->flow_rate_s * 60.0f;
    return fs->flow_rate_m;
}

float FlowSensor_GetFlowRate_s(FlowSensor *fs) {
    return fs->flow_rate_s;
}

float FlowSensor_GetVolume(FlowSensor *fs) {
    return fs->volume;
}

void FlowSensor_ResetPulse(FlowSensor *fs) {
    fs->pulse = 0;
    fs->total_pulse = 0;
}

void FlowSensor_ResetVolume(FlowSensor *fs) {
    fs->volume = 0;
}
