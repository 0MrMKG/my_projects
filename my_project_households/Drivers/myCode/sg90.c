#include "stm32f1xx_hal.h"
#include "driver_timer.h"
extern TIM_HandleTypeDef htim1;
void DuoJi_Angle_TIM1(int angle)
 {
	 int  PWM;
	 PWM = angle/180*250 ;
     __HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1,PWM);
 }
void Test_For_sg90()
{
	
	while(1)
	{
	DuoJi_Angle_TIM1(0);	// 0¡ã £¬CCR = 50
	mdelay(500);
	DuoJi_Angle_TIM1(45);	// 0¡ã £¬CCR = 50
	mdelay(500);
	DuoJi_Angle_TIM1(90);	// 0¡ã £¬CCR = 50
	mdelay(500);
	DuoJi_Angle_TIM1(180);	// 0¡ã £¬CCR = 50
	mdelay(500);

	}

}