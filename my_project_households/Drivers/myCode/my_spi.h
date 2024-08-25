#include "main.h"

#ifndef _SPI_H_
#define _SPI_H_

#define u8 uint8_t
 
u8 SPI_WriteByte(SPI_TypeDef* SPIx,u8 Byte);
void SPI_Init(void);
void SPI_SetSpeed(SPI_TypeDef* SPIx,u8 SpeedSet);

#endif
