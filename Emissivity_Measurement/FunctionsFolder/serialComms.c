/*
 * serialComms.c
 *
 *  Created on: Apr 1, 2021
 *      Author: mmartinn
 */

#include "main.h"
#include "temperature.h"
#include <string.h>

void debugPrint(UART_HandleTypeDef *huart, char _out[]) {
	HAL_UART_Transmit_IT(huart, (uint8_t*) _out, strlen(_out));
}

void debugPrintln(UART_HandleTypeDef *huart, char _out[]) {
	// HAL_UART_Transmit_IT(huart, (uint8_t *) _out, strlen(_out));
	HAL_UART_Transmit(huart, (uint8_t*) _out, strlen(_out), HAL_MAX_DELAY);
	char newline[1] = "\n";
	// HAL_UART_Transmit_IT(huart, (uint8_t *) newline, 2);
	HAL_UART_Transmit(huart, (uint8_t*) newline, 1, HAL_MAX_DELAY);
}

void setupSerial(UART_HandleTypeDef *huart) {

	__HAL_UART_ENABLE_IT(huart, UART_IT_IDLE);
}

int parseSerialCmd(char *recMsg, int size) {
	char str[5];
	char MSG[90] = { '\0' };
	char cRate[7];
	char DACChannel;
	char cDACValue[7];
	float DACVoltage;


	switch (recMsg[0]) {
	case 'T':
		// Temperature read-out
		sprintf(MSG, "%d", temperaturePulses);
		debugPrintln(&huart2, MSG);
		break;
	case 'S':
		// Start acquisition
		sprintf(MSG, "Start acquisition");
		debugPrintln(&huart2, MSG);
		startADC_Acquisition();
		break;
	case 's':
		// Stop acquisition
		stopADC_Acquisition();
		sprintf(MSG, "Stop acquisition");
		debugPrintln(&huart2, MSG);
		break;
	case 'R':
		// Set rate in us
		if (recMsg[1] == '?') {
			uint32_t timerFreq = HAL_RCC_GetSysClockFreq() / (TIM2->PSC + 1);
			uint32_t strRate = TIM2->ARR * (1e6 / timerFreq) + 1;
			sprintf(MSG, "Rate: %d us", strRate);
			debugPrintln(&huart2, MSG);
		} else {
			memcpy(cRate, &recMsg[1], 6);
			cRate[6] = '\0';
			uint32_t rate = atoi(cRate);
			setADCMeasRate_us(rate);
			sprintf(MSG, "Capturing data every %d us", rate);
			debugPrintln(&huart2, MSG);
		}
		break;
	case 'O':
		// Set DAC offset
		if ((recMsg[1] > 47) && (recMsg[1] < 58)) { // If a digit
			if ((recMsg[2] == ',')) {
				DACChannel = recMsg[1] - 48;
				memcpy(cDACValue, &recMsg[3], 6);
				DACVoltage = (float) atoi(cDACValue) / 1000;
				DACVoltage = SetDACOutputVoltage(DACChannel, DACVoltage);
				sprintf(MSG, "DAC%d: %fV", DACChannel, DACVoltage);
				debugPrintln(&huart2, MSG);
			}

		}

		break;
	case 'M':
		// Controlled current in mA
		if (recMsg[1] == '1') {
			if ((recMsg[2] == ',')) {
				memcpy(cDACValue, &recMsg[3], 6);
				DACVoltage = (float) atoi(cDACValue) / 1000;
				DACVoltage = SetDACOutputVoltage(DAC_CHANNEL_R0REF, DACVoltage);
				sprintf(MSG, "R0 current: %fmA", DACVoltage*1000);
				debugPrintln(&huart2, MSG);

				HAL_GPIO_WritePin(R0MeasON_GPIO_Port, R0MeasON_Pin, GPIO_PIN_SET);
				//HAL_Delay(1);
				startADC_Acquisition();

			}



		}
		else if(recMsg[1] == '0'){

			stopADC_Acquisition();
			HAL_GPIO_WritePin(R0MeasON_GPIO_Port, R0MeasON_Pin, GPIO_PIN_RESET);
			SetDACOutputVoltage(DAC_CHANNEL_R0REF, 0);

			sprintf(MSG, "Stop R0 measurement");
			debugPrintln(&huart2, MSG);
		}

		break;
	case 'A':

		startADC_Acquisition();

		break;
	case 'P':

		if (recMsg[1] == '1') {
			// Turn on main transistors
			HAL_GPIO_WritePin(WireON_GPIO_Port, WireON_Pin, GPIO_PIN_SET);
			// Just in case turn off R0Meas circuit
			HAL_GPIO_WritePin(R0MeasON_GPIO_Port, R0MeasON_Pin, GPIO_PIN_RESET);

			}

		else if(recMsg[1] == '0'){
			// Turn off main transistors, also R0Meas circuit
			HAL_GPIO_WritePin(WireON_GPIO_Port, WireON_Pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(R0MeasON_GPIO_Port, R0MeasON_Pin, GPIO_PIN_RESET);

		}

		break;
	default:
		break;
	}

	return (0);

}
