#ifndef __BLUETOOTH_H__
#define __BLUETOOTH_H__
 
#include "main.h" //HAL���ļ�����
 
extern UART_HandleTypeDef huart1;//����USART2��HAL��ṹ��
 
#define USART1_REC_LEN  200//����USART2�������ֽ���
 
extern uint8_t  USART1_RX_BUF[USART1_REC_LEN];//���ջ���,���USART_REC_LEN���ֽ�.ĩ�ֽ�ΪУ���
extern uint16_t USART1_RX_STA;//����״̬���
extern uint8_t USART1_NewData;//��ǰ�����жϽ��յ�1���ֽ����ݵĻ���
 
 
void  HAL_UART_RxCpltCallback(UART_HandleTypeDef  *huart);//�����жϻص���������
 
#endif 
 
 