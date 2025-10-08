
#ifndef INC_FLOWSENSOR_H_
#define INC_FLOWSENSOR_H_


#include "stm32u5xx_hal.h"   // or stm32xxxx_hal.h depending on your MCU

typedef struct {
    uint16_t pulse_per_liter;   // calibration value
    volatile uint32_t pulse;    // ISR counter
    uint32_t total_pulse;
    uint32_t last_time_ms;
    float flow_rate_s;          // L/s
    float flow_rate_m;          // L/min
    float flow_rate_h;          // L/h
    float volume;               // Liters
    GPIO_TypeDef *GPIOx;        // Port of sensor pin
    uint16_t GPIO_Pin;          // Pin number
} FlowSensor;

/* Initialization */
void FlowSensor_Init(FlowSensor *fs, uint16_t type, GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

/* ISR counter */
void FlowSensor_Count(FlowSensor *fs);

/* Read and update calculations */
void FlowSensor_Read(FlowSensor *fs, int32_t calibration);

/* Getters */
uint32_t FlowSensor_GetPulse(FlowSensor *fs);
float FlowSensor_GetFlowRate_h(FlowSensor *fs);
float FlowSensor_GetFlowRate_m(FlowSensor *fs);
float FlowSensor_GetFlowRate_s(FlowSensor *fs);
float FlowSensor_GetVolume(FlowSensor *fs);

/* Reset */
void FlowSensor_ResetPulse(FlowSensor *fs);
void FlowSensor_ResetVolume(FlowSensor *fs);


#endif /* INC_FLOWSENSOR_H_ */
