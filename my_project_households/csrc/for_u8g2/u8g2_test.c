#include "u8g2_test.h"
#include "FreeRTOS.h"
#include "task.h"
//---------------U8g2���Ժ���

#define SEND_BUFFER_DISPLAY_MS(u8g2, ms)\
  do {\
    u8g2_SendBuffer(u8g2); \
    HAL_Delay(ms);\
  }while(0);


//��������ʾ
void testDrawProcess(u8g2_t *u8g2)
{
	for(int i=10;i<=80;i=i+2)
	{
		u8g2_ClearBuffer(u8g2); 
			
		char buff[20];
		
		u8g2_SetFont(u8g2,u8g2_font_ncenB12_tf);
		u8g2_DrawStr(u8g2,16,32,"WAITING...");//�ַ���ʾ
		
		u8g2_SetFont(u8g2,u8g2_font_ncenB08_tf);
		u8g2_DrawStr(u8g2,100,49,buff);//��ǰ������ʾ
		
		u8g2_DrawRBox(u8g2,16,40,i,10,4);//Բ��������ο�
		u8g2_DrawRFrame(u8g2,16,40,80,10,4);//Բ�Ǿ���
		
		u8g2_SendBuffer(u8g2);
	}
	vTaskDelay(100);
}


//������� ����Ӣ�Ŀ�ѡ�� u8g2_font_ncenB..(��) ϵ������
//u8g2_font_unifont_t_symbols/u8g2_font_unifont_h_symbols(ϸ Բ��)
void testShowFont(u8g2_t *u8g2)
{
	int t = 1000;
	char testStr[14] = "STM32F103C8T6";
	
	u8g2_ClearBuffer(u8g2);
	
	u8g2_SetFont(u8g2,u8g2_font_u8glib_4_tf);
	u8g2_DrawStr(u8g2,0,5,testStr);
	SEND_BUFFER_DISPLAY_MS(u8g2,t);
	
	u8g2_SetFont(u8g2,u8g2_font_ncenB08_tf);
	u8g2_DrawStr(u8g2,0,30,testStr);
	SEND_BUFFER_DISPLAY_MS(u8g2,t);
	
    u8g2_SetFont(u8g2,u8g2_font_ncenB10_tr);
	u8g2_DrawStr(u8g2,0,60,testStr);
	SEND_BUFFER_DISPLAY_MS(u8g2,t);
}

//�����ľ���
void testDrawFrame(u8g2_t *u8g2)
{
	int t = 1000;
	int x = 16;
	int y = 32;
}


