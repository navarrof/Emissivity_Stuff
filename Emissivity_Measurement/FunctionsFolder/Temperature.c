/*
 * Temperature.c
 *
 *  Created on: Apr 20, 2021
 *      Author: mmartinn
 */

#include "temperature.h"

void setupTemperature(void) {
	HAL_LPTIM_Counter_Start(&hlptim1, 0xFFFF);
	HAL_LPTIM_Counter_Start(&hlptim2, 0xFFFF);
}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
	if (GPIO_Pin == Temp1Gate_Pin) {
		//temperature1 = pulsesToTemperature(LPTIM1->CNT);
		uint16_t temp = LPTIM1->CNT;
		temperaturePulses &= 0x000FFF;
		temperaturePulses += (temp << 12);
		newTemp = 1;
		HAL_LPTIM_Counter_Stop(&hlptim1);
		HAL_LPTIM_Counter_Start(&hlptim1, 0xFFFF);

	} else if (GPIO_Pin == Temp2Gate_Pin) {
		//temperature1 = pulsesToTemperature(LPTIM1->CNT);
		uint16_t temp = LPTIM2->CNT;
		temperaturePulses &= 0xFFF000;
		temperaturePulses += temp;
		newTemp = 1;

		HAL_LPTIM_Counter_Stop(&hlptim2);
		HAL_LPTIM_Counter_Start(&hlptim2, 0xFFFF);

	}

}

float pulsesToTemperature(uint32_t pulses) {

	int LUT_temperature[21][2] = {
			{ -50, 26 },
			{ -40, 181 },
			{ -30, 338 },
			{ -20, 494 },
			{ -10, 651 },
			{ 0, 808 },
			{ 10, 966 },
			{ 20, 1125 },
			{ 30, 1284 },
			{ 40, 1443 },
			{ 50, 1602 },
			{ 60, 1762 },
			{ 70, 1923 },
			{ 80, 2084 },
			{ 90, 2245 },
			{ 100, 2407 },
			{ 110, 2569 },
			{ 120, 2731 },
			{ 130, 2893 },
			{ 140, 3057 },
			{ 150, 3218 },
	};

	if (pulses < LUT_temperature[0][1]) {
		return (-50.0);
	} else if (pulses > LUT_temperature[20][1]) {
		return (150.0);
	}

	int row = 0;
	float temperature = 0;
	/* Scan the LUT for the starting temperature to interpolate */
	while (LUT_temperature[row][1] < pulses) {
		row++;
	}
	/* Get the surrounding points in the LUT (temperature, pulses) */
	int TLow = LUT_temperature[row - 1][0];
	int THigh = LUT_temperature[row][0];
	int pulsesLow = LUT_temperature[row - 1][1];
	int pulsesHigh = LUT_temperature[row][1];
	float deltaT = (float) ((THigh - TLow) / (float) (pulsesHigh - pulsesLow));
	/* Calculate temperature */
	temperature = TLow + deltaT * (pulses - pulsesLow);

	return (temperature);
}
