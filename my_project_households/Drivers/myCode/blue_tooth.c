#include "blue_tooth.h"
 
uint8_t USART1_RX_BUF[USART1_REC_LEN];//���ջ���,���USART_REC_LEN���ֽ�.
uint16_t USART1_RX_STA=0;//����״̬���//bit15��������ɱ�־��bit14~0�����յ�����Ч�ֽ���Ŀ
uint8_t USART1_NewData;//��ǰ�����жϽ��յ�1���ֽ����ݵĻ���
 
void  HAL_UART_RxCpltCallback(UART_HandleTypeDef  *huart)//�����жϻص�����
{
    if(huart ==&huart1)
    {
        if((USART1_RX_STA&0x8000)==0)//����δ���
        {
            if(USART1_NewData==0x5A)//���յ���0x5A
            {
                 USART1_RX_STA|=0x8000;   //��������ˣ���USART2_RX_STA�е�bit15��15λ����1
            }
            else
            {
                   USART1_RX_BUF[USART1_RX_STA&0X7FFF]=USART1_NewData; //���յ������ݷ������飬
                   USART1_RX_STA++;  //���ݳ��ȼ�����1
                   if(USART1_RX_STA>(USART1_REC_LEN-1))USART1_RX_STA=0;//�������ݴ���,���¿�ʼ����
 
            }
        }
        HAL_UART_Receive_IT(&huart1,(uint8_t *)&USART1_NewData,1); //��Ϊÿִ����һ���жϻص������Ὣ�����жϹ��ܹرգ����������Ҫ�ٿ��������ж�
 
 
    }
}
 