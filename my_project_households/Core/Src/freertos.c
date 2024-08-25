/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * File Name          : freertos.c
  * Description        : Code for freertos applications
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "FreeRTOS.h"
#include "task.h"
#include "main.h"
#include "cmsis_os.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
//------------freertos------------
#include "cmsis_os.h"
#include "FreeRTOS.h"                   // ARM.FreeRTOS::RTOS:Core
#include "task.h"                       // ARM.FreeRTOS::RTOS:Core
#include "event_groups.h"               // ARM.FreeRTOS::RTOS:Event Groups
#include "semphr.h"                     // ARM.FreeRTOS::RTOS:Core
//------------private(hardware)------------
#include "driver_timer.h"
#include "driver_lcd.h"
#include "driver_led.h"
#include "sg90.h"
#include "music.h"
#include "blue_tooth.h"
#include "driver_ir_receiver.h"
#include "driver_ir_sender.h"
#include "driver_passive_buzzer.h"
#include "driver_dht11.h"
#include "driver_light_sensor.h"
#include "spi_lcd_test.h"
#include "lcd_spi.h"
#include "lcd.h"
#include "u8g2_test.h"
#include "stm32_u8g2.h"
#include "gui.h"
//------------private(game)------------
#include "game1.h"
#include "english.h"
#include "resources.h"
#include "draw.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN Variables */
//---------------------------------------------
// ---------------- Variables ----------------
//extern uint8_t rx_buf[2];
//extern uint8_t Bluetooth_data;
//static StackType_t g_pucStackOfLightTask[128*4];
//static StaticTask_t g_TCBofLightTask;
//static TaskHandle_t LightTask;
//static StackType_t g_pucStackOfLightTask2[128*4];
//static StaticTask_t g_TCBofLightTask2;
//static TaskHandle_t LightTask2;
//---------------------------------------------
//// ---------------- global queues ----------------
//static QueueHandle_t key_queue;
//static QueueHandle_t big_data_queue;
//// ---------------- queue set----------------
//static QueueSetHandle_t queue_set_handle;
//	static QueueHandle_t queue_set_1queue_handle;
//	static QueueHandle_t queue_set_2semphore_handle;
//// ---------------- semphore ----------------
//static QueueHandle_t semphore_handle;
//static QueueHandle_t count_semphore_handle;
//static QueueHandle_t mutex_semphore_handle;
//  //---------------- eventgroups init --------------------
//static EventGroupHandle_t eventgroup_handle;
//---------------------------------------------
//---------------------------------------------
//---------------------------------------------

/* USER CODE END Variables */
/* Definitions for defaultTask */
osThreadId_t defaultTaskHandle;
const osThreadAttr_t defaultTask_attributes = {
  .name = "defaultTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */
// ---------------- task functions ----------------
void start_task_1(void *params);
void start_task_2(void *params);
void start_task_3(void *params);
void general_task(void *params);
void DHT11_task(void *params);
void LightSensor_task(void *params);

//// ---------------- LCD test function ----------------
//// same function for different tasks -experiment
//struct TaskInfo {
//	uint8_t x;
//	uint8_t y;
//	char name[16];
//};
//// ----------------global_params_for_tasks----------------
//static struct TaskInfo OledTask1 = {0,0,"SHIT_1"};
//static struct TaskInfo OledTask2 = {0,3,"SHIT_2"};
//static struct TaskInfo OledTask3 = {0,6,"SHIT_3"};
//static int g_LCD_CAN_USE = 1;
//void LCD_Print_Task(void *params)
//{
//	int len;
//	uint32_t cnt = 0;
//	struct TaskInfo *printInfo = params;
//	while(1)
//	{
//		if (g_LCD_CAN_USE)
//		{
//		g_LCD_CAN_USE = 0;
//		len = LCD_PrintString(printInfo->x,printInfo->y,printInfo->name);
//		len += LCD_PrintString(len,printInfo->y,":");
//		LCD_PrintSignedVal(len,printInfo->y,cnt++);
//		g_LCD_CAN_USE = 1;
//		}
//		mdelay(500);
//	}
//}



/* USER CODE END FunctionPrototypes */

void StartDefaultTask(void *argument);

void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */

/**
  * @brief  FreeRTOS initialization
  * @param  None
  * @retval None
  */
void MX_FREERTOS_Init(void) {
  /* USER CODE BEGIN Init */
	TaskHandle_t xSoundTaskhandle;
	TaskHandle_t start_task_1_handle;
	TaskHandle_t start_task_2_handle;
	TaskHandle_t start_task_3_handle;
	TaskHandle_t general_task_handle;
	LCD_Init();
	LCD_Clear();
	IRReceiver_Init();
	LCD_PrintString(0,0,"OK");
	spi_LCD_Init();
	
  /* USER CODE END Init */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  //---------------------------------------------
  //---------------- queue ---------------------
//  #define key_queue_length 2
//  #define key_queue_item_size sizeof(uint8_t)
//  key_queue = xQueueCreate(key_queue_length,key_queue_item_size);
//  
//  #define big_data_queue_length 1
//  #define big_data_queue_item_size sizeof(char*)
//  big_data_queue = xQueueCreate(10,10);
  //---------------- queue set ---------------------
//  queue_set_handle = xQueueCreateSet(2);
//	queue_set_1queue_handle = xQueueCreate(1,sizeof(uint8_t));
//	queue_set_2semphore_handle = xSemaphoreCreateBinary();
//  xQueueAddToSet(queue_set_1queue_handle,queue_set_handle);
//  xQueueAddToSet(queue_set_2semphore_handle,queue_set_handle);
  //---------------- semphores --------------------
//  semphore_handle = xSemaphoreCreateBinary();
//  count_semphore_handle = xSemaphoreCreateCounting(100,0);
//  mutex_semphore_handle = xSemaphoreCreateMutex();
  //---------------- eventgroups init --------------------
//  eventgroup_handle = xEventGroupCreate();
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* creation of defaultTask */
  defaultTaskHandle = osThreadNew(StartDefaultTask, NULL, &defaultTask_attributes);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  
 // --------------------tasks--------------------
 
//   xTaskCreate(LightSensor_task, "test_Task", 128, NULL, osPriorityNormal, &general_task_handle);  

   
   
   
   
   
   
   
   
   
   
   
   
   
   
// ----------------------------------------------------------------------------------------------
  /*------1-1 music or lcd------*/
//  xTaskCreate(game1_task, "GameTask", 128, NULL, osPriorityNormal, NULL);
//  xTaskCreate(play_music,"music",128,NULL,osPriorityAboveNormal,&xSoundTaskhandle);
//  xTaskCreate(LCD_Print_Test,"std",128,NULL,osPriorityAboveNormal,&xSoundTaskhandle);
  /*------1-2 LED F11------*/
//  LightTask = xTaskCreateStatic(Led_Test,"led",128,NULL,osPriorityAboveNormal,g_pucStackOfLightTask,&g_TCBofLightTask);
  /*------1-3 LED F12------*/
//  LightTask2 = xTaskCreateStatic(Led_Test_2,"led2",128,NULL,osPriorityAboveNormal,g_pucStackOfLightTask2,&g_TCBofLightTask2);
  /*------1-4 create different tasks using same function------*/
//	xTaskCreate(LCD_Print_Task,"oled_task3",128,&OledTask1,osPriorityAboveNormal,NULL);
//	xTaskCreate(LCD_Print_Task,"oled_task2",128,&OledTask2,osPriorityAboveNormal,NULL);
//	xTaskCreate(LCD_Print_Task,"oled_task3",128,&OledTask3,osPriorityAboveNormal,NULL);
// ----------------------------------------------------------------------------------------------
	
	
	
  /* USER CODE END RTOS_THREADS */

  /* USER CODE BEGIN RTOS_EVENTS */
  /* add events, ... */
  /* USER CODE END RTOS_EVENTS */

}

/* USER CODE BEGIN Header_StartDefaultTask */
/**
  * @brief  Function implementing the defaultTask thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_StartDefaultTask */
void StartDefaultTask(void *argument)
{
  /* USER CODE BEGIN StartDefaultTask */
  /* Infinite loop */
	
	
//	LightSensor_Test();
	

	while(1)
	{
	LCD_Fill(0,0,lcddev.width,lcddev.height,WHITE);
//	Show_Str(0,25,BLUE,YELLOW,"BL Test",16,1);
	Pic_test();
	vTaskDelay(1000);
	}

	
	
	
//  -------------------------------------------------------------------------
//  ----------------------demo3     DHT11      test--------------------------
//  -------------------------------------------------------------------------
	
//	int hum, temp;
//    int len;
//	char display_buf[12];
//	u8g2_t u8g2;
//	
//	DHT11_Init();
//	u8g2Init(&u8g2);
//	
//	while (1)
//	{
//		if (DHT11_Read(&hum, &temp) !=0 )
//		{
//			DHT11_Init();
//		}
//		else
//		{	
//	   u8g2_DrawFrame(&u8g2,0,0,5,10);
//	   u8g2_DrawFrame(&u8g2,0,20,5,10);
//			
//	   u8g2_SendBuffer(&u8g2);	
//	   u8g2_SetFont(&u8g2,u8g2_font_DigitalDiscoThin_tf);
//	   sprintf((char*)display_buf,"temp:      %d",temp);
//	   u8g2_DrawStr(&u8g2,10,10,display_buf);
//	
//	   u8g2_SetFont(&u8g2,u8g2_font_DigitalDiscoThin_tf);
//	   sprintf((char*)display_buf,"humidity:  %d%c",hum ,'%');
//	   u8g2_DrawStr(&u8g2,10,30,display_buf);
//	   u8g2_SendBuffer(&u8g2);

//		}
//		mdelay(2000);  /* 读取周期是2S, 不能读太频繁 */
//	}
	

	
	
//  -------------------------------------------------------------------------
//  ----------------------demo2-----------u8g2 test--------------------------
//  -------------------------------------------------------------------------
//    u8g2_t u8g2; // a structure which will contain all the data for one display
//    u8g2Init(&u8g2);
//	while(1)
//	{
//	   u8g2_SendBuffer(&u8g2);
////	   u8g2_DrawBox(&u8g2,0,0,20,20);
//	   u8g2_DrawCircle(&u8g2,30,30,10,0x15);
////	   u8g2_DrawBox(&u8g2,20,20,20,20);
//	   u8g2_SendBuffer(&u8g2);
//	   u8g2_DrawFrame(&u8g2,10,40,20,20);
//	   u8g2_SendBuffer(&u8g2);
//	   u8g2_SetFont(&u8g2,u8g2_font_DigitalDiscoThin_tf);
//	   u8g2_DrawStr(&u8g2,30,10,"Hello World");
//	   u8g2_SendBuffer(&u8g2);
//	   HAL_Delay(1000);
//	}



//  -------------------------------------------------------------------------
//  ----------------------demo 01用红外遥控控制音乐--------------------------
//  -------------------------------------------------------------------------
//  uint8_t dev, data;
//  int len;
//	int bRunning;
//	
//	TaskHandle_t xSoundTaskHandle = NULL;
//	BaseType_t ret;
//	
//	LCD_Init();
//	LCD_Clear();

//	
//    IRReceiver_Init();
//	LCD_PrintString(0, 0, "Waiting control");

//    while (1)
//    {
//        /* 读取红外遥控器 */
//		if (0 == IRReceiver_Read(&dev, &data))
//		{		
//			if (data == 0xa8) /* play */
//			{
//				/* 创建播放音乐的任务 */
//			  if (xSoundTaskHandle == NULL)
//			  {
//					LCD_ClearLine(0, 0);
//					LCD_PrintString(0, 0, "Create Task");
//					ret = xTaskCreate(play_music, "SoundTask", 128, NULL, osPriorityNormal+1, &xSoundTaskHandle);
//					bRunning = 1;
//			  }
//			  else
//			  {
//				  /* 要么suspend要么resume */
//				  if (bRunning)
//				  {
//					  LCD_ClearLine(0, 0);
//					  LCD_PrintString(0, 0, "Suspend Task");
//					  vTaskSuspend(xSoundTaskHandle);
//					  PassiveBuzzer_Control(0); /* 停止蜂鸣器 */
//					  bRunning = 0;
//				  }
//				  else
//				  {
//					  LCD_ClearLine(0, 0);
//					  LCD_PrintString(0, 0, "Resume Task");
//					  vTaskResume(xSoundTaskHandle);
//					  bRunning = 1;
//				  }
//			  }
//			}
//			
//			else if (data == 0xa2) /* power */
//			{
//				/* 删除播放音乐的任务 */
//				if (xSoundTaskHandle != NULL)
//				{
//					LCD_ClearLine(0, 0);
//					LCD_PrintString(0, 0, "Delete Task");
//					vTaskDelete(xSoundTaskHandle);
//					PassiveBuzzer_Control(0); /* 停止蜂鸣器 */
//					xSoundTaskHandle = NULL;
//				}
//			}
//		}
//    }
//  -------------------------------------------------------------------------
//  -------------------------------------------------------------------------
  /* USER CODE END StartDefaultTask */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */


//-------------------------------------------------------------------------
//----------------------------队列实验-------------------------------------
//-------------------------------------------------------------------------
//void start_task_1(void *params)
//{
//	//just for test
//	char gigi[100] = {"heeloooolleoolelelooleloooolellooo"};
//	char * buf;
//	buf = &gigi[0];
//	BaseType_t err2 = 0;
//	
//	BaseType_t err = 0;
//	uint8_t dev, data;
//	uint8_t count = 0;
//	int len;
//    while (1)
//    {
//		if (!IRReceiver_Read(&dev, &data))
//		{	
//			// transfer the key data
//			if (data == 0x4a)
//			{
//				LCD_ClearLine(0,0);
//				err = xQueueSend(key_queue,&data,portMAX_DELAY);
//				if (err != pdTRUE)
//				{
//				   LCD_PrintString(0,0,"GG");
//				}
//				else
//				{
//				   LCD_PrintHex(6,0,++count,1);
//				}
//			}
//			// transfer the address of bigdata
////			if (data == 0x52)
////			{
////				LCD_ClearLine(0,2);
////				err2 = xQueueSend(big_data_queue,&buf,portMAX_DELAY);
////				if (err2 != pdTRUE)
////				{
////				   LCD_PrintString(0,2,"GG");
////				}
////				LCD_PutChar(6,2,*buf);
////			}	
//		}
//		vTaskDelay(10);
//	}
//}

//void start_task_2(void *params)
//{
//	
//	uint8_t key_num = 0;
//	BaseType_t err = 0;
//	while(1)
//	{
//		//out queue
//		err = xQueueReceive(key_queue,&key_num,portMAX_DELAY);
//		if (err != pdTRUE)
//		{
//		    LCD_PrintString(0,3,"GG");
//		}
//		else
//		{
//			LCD_PrintHex(0,3,key_num,1);	
//		}
//		
//	}
//	
//}
//-------------------------------------------------------------------------
//-------------------------------------------------------------------------


//-------------------------------------------------------------------------
//----------------------------二值信号量实验--------------------------------
//-------------------------------------------------------------------------

//void start_task_1(void *params)
//{
//	BaseType_t err = 0;
//	uint8_t dev, data;
//	int len;
//	while(1)
//	{
//		if (!IRReceiver_Read(&dev, &data))
//		{	
//			// transfer the key data
//			if (data == 0x4a)
//			{
//				LCD_ClearLine(0,0);
//				if (semphore_handle!= NULL)
//				{
//					err = xSemaphoreGive(semphore_handle);
//					if (err == pdPASS)
//					{
//					LCD_PrintString(0,0,"win");
//					}
//					else
//					{
//					LCD_PrintString(0,0,"lose");
//					}
//				}
//				
//			}
//		}
//		vTaskDelay(10);
//	}
//	
//}

//void start_task_2(void *params)
//{
//	BaseType_t err = 0;
//	int len = 0;
//	while(1)
//	{
//		xSemaphoreTake(semphore_handle,1000);
//		if (err == pdTRUE)
//		{
//			LCD_PrintString(0,2,"success");
//		}
//		else
//		{
//			LCD_PrintString(8,2,"timeout");
//			LCD_PrintHex(0,4,++len,10);
//		}
//	}
//}

//-------------------------------------------------------------------------
//-------------------------------------------------------------------------


//-------------------------------------------------------------------------
//----------------------------计数型信号量实验------------------------------
//-------------------------------------------------------------------------

//void start_task_1(void *params)
//{
//	BaseType_t err = 0;
//	uint8_t dev, data;
//	int len;
//	while(1)
//	{
//		if (!IRReceiver_Read(&dev, &data))
//		{	
//			// transfer the key data
//			if (data == 0x4a)
//			{
//				LCD_ClearLine(0,0);
//				if (count_semphore_handle!= NULL)
//				{
//					err = xSemaphoreGive(count_semphore_handle);
//					if (err == pdPASS)
//					{
//					LCD_PrintString(0,0,"win");
//					}
//					else
//					{
//					LCD_PrintString(0,0,"lose");
//					}
//				}
//				
//			}
//		}
//		vTaskDelay(10);
//	}
//	
//}

//void start_task_2(void *params)
//{
//	BaseType_t err = 0;
//	int len = 0;
//	while(1)
//	{
//		err = xSemaphoreTake(count_semphore_handle,portMAX_DELAY);
//		vTaskDelay(1000);
//		if (err == pdTRUE)
//		{
//			LCD_PrintString(0,2,"OK");
//			LCD_PrintHex(4,2,uxSemaphoreGetCount(count_semphore_handle),10);
//		}
//		else
//		{
//			LCD_PrintString(0,2,"ERROR");
//		}
//	}
//}
//-------------------------------------------------------------------------
//-------------------------------------------------------------------------

//-------------------------------------------------------------------------
//----------------------------互斥信号量实验-------------------------------
//-------------------------------------------------------------------------
//void start_task_1(void *params)
//{
//	BaseType_t err = 0;
//	uint8_t dev, data;
//	int len;
//	while(1)
//	{
//		LCD_PrintString(0,0,"low_getting");
//		xSemaphoreTake(mutex_semphore_handle,portMAX_DELAY);
//		LCD_ClearLine(0,0);
//		LCD_PrintString(0,0,"low_running");
//		mdelay(3000);
//		LCD_ClearLine(0,0);
//		LCD_PrintString(0,0,"low_emitting");
//		vTaskDelay(1000);
//	}
//	
//}

//void start_task_2(void *params)
//{
//	while(1)
//	{
//		LCD_PrintString(0,2,"middle running");
//		vTaskDelay(1000);
//	}
//}

//void start_task_3(void *params)
//{
//	while(1)
//	{
//		LCD_PrintString(0,4,"high_getting");
//		xSemaphoreTake(mutex_semphore_handle,portMAX_DELAY);
//		LCD_ClearLine(0,0);
//		LCD_PrintString(0,4,"high_running");
//		mdelay(3000);
//		LCD_ClearLine(0,0);
//		LCD_PrintString(0,4,"high_emitting");
//		vTaskDelay(1000);
//	}
//}


//-------------------------------------------------------------------------
//----------------------------队列集实验-----------------------------------
//-------------------------------------------------------------------------


//void start_task_1(void *params)
//{
//	BaseType_t err = 0;
//	uint8_t dev, data;
//	int len;
//	while(1)
//	{
//		if (!IRReceiver_Read(&dev, &data))
//		{	
//			// transfer the key data
//			if (data == 0x4a)
//			{
//				xQueueSend(queue_set_1queue_handle,&data,portMAX_DELAY);
//			}
//			else if (data == 0x52)
//			{
//				xSemaphoreGive(queue_set_2semphore_handle);
//			}
//		}
//		vTaskDelay(10);
//	}	
//}

//void start_task_2(void *params)
//{
//	QueueSetMemberHandle_t member_handle;
//	uint8_t key;
//	while(1)
//	{
//		member_handle = xQueueSelectFromSet(queue_set_handle,portMAX_DELAY);
//		if (member_handle == queue_set_1queue_handle)
//		{
//			xQueueReceive(member_handle,&key,portMAX_DELAY);
//			LCD_PrintString(0,0,"get key data");
//		}
//		else if (member_handle == queue_set_2semphore_handle)
//		{
//			xSemaphoreTake(member_handle,portMAX_DELAY);
//			LCD_PrintString(0,2,"get Semaphore");
//		}
//	}
//}

void general_task(void *params)
{
	BaseType_t err = 0;
	uint8_t dev, data;
	int len;
	TaskHandle_t start_task_1_handle;
	while(1)
	{
		if (!IRReceiver_Read(&dev, &data))
		{	
			// transfer the key data
			if (data == 0xe2 )
			{
				
			}

		}
		vTaskDelay(10);
	}	

}


//外设：无源蜂鸣器播放音乐。
void start_task_1(void *params)
{
    uint8_t dev, data;
    int len;
	int bRunning;
	TaskHandle_t xSoundTaskHandle = NULL;
	BaseType_t ret;
	LCD_PrintString(0, 0, "Waiting control");
    while (1)
    {
        /* 读取红外遥控器 */
		if (0 == IRReceiver_Read(&dev, &data))
		{		
			if (data == 0xa8) /* play */
			{
				/* 创建播放音乐的任务 */
			  if (xSoundTaskHandle == NULL)
			  {
					LCD_ClearLine(0, 0);
					LCD_PrintString(0, 0, "Create Task");
					ret = xTaskCreate(play_music, "SoundTask", 128, NULL, osPriorityNormal+1, &xSoundTaskHandle);
					bRunning = 1;
			  }
			  else
			  {
				  /* 要么suspend要么resume */
				  if (bRunning)
				  {
					  LCD_ClearLine(0, 0);
					  LCD_PrintString(0, 0, "Suspend Task");
					  vTaskSuspend(xSoundTaskHandle);
					  PassiveBuzzer_Control(0); /* 停止蜂鸣器 */
					  bRunning = 0;
				  }
				  else
				  {
					  LCD_ClearLine(0, 0);
					  LCD_PrintString(0, 0, "Resume Task");
					  vTaskResume(xSoundTaskHandle);
					  bRunning = 1;
				  }
			  }
			}
			
			else if (data == 0xb0) /* C */
			{
				/* 删除播放音乐的任务 */
				if (xSoundTaskHandle != NULL)
				{
					LCD_ClearLine(0, 0);
					LCD_PrintString(0, 0, "Delete Task");
					vTaskDelete(xSoundTaskHandle);
					PassiveBuzzer_Control(0); /* 停止蜂鸣器 */
					xSoundTaskHandle = NULL;
				}
			}
		}
	}
}



void start_task_2(void *params)
{
	while(1)
	{
	
	}

}

void start_task_3(void *params)
{
	while(1)
	{

	}
}
//---------------------------------------------------
//--------------------HARDWARE_TASKS-----------------
//---------------------------------------------------
// 001 DHT_Task(online when it is called by lobby)
void DHT11_task(void *params)
{
	int hum, temp;
    int len;
	char display_buf[12];
	u8g2_t u8g2;
	
	DHT11_Init();
	u8g2Init(&u8g2);
	
	while (1)
	{
		if (DHT11_Read(&hum, &temp) !=0 )
		{
			DHT11_Init();
		}
		else
		{	
//	   u8g2_DrawFrame(&u8g2,0,0,5,10);
//	   u8g2_DrawFrame(&u8g2,0,20,5,10);		
//	   u8g2_SendBuffer(&u8g2);	
//	   u8g2_SetFont(&u8g2,u8g2_font_DigitalDiscoThin_tf);
//	   sprintf((char*)display_buf,"temp:      %d",temp);
//	   u8g2_DrawStr(&u8g2,10,10,display_buf);
//	   u8g2_SetFont(&u8g2,u8g2_font_DigitalDiscoThin_tf);
//	   sprintf((char*)display_buf,"humidity:  %d%c",hum ,'%');
//	   u8g2_DrawStr(&u8g2,10,30,display_buf);
//	   u8g2_SendBuffer(&u8g2);
		}
		mdelay(2000);  /* 读取周期是2S, 不能读太频繁 */
	}
}

void LightSensor_task(void *params)
{

	LightSensor_Test();

}

//---------------------------------------------------
//---------------------------------------------------
//---------------------------------------------------
/* USER CODE END Application */

