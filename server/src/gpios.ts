import { Gpio } from 'onoff';  

//set pins
export const motorENA = new Gpio(25,'out');
export const motorIN1 = new Gpio(23,'out');
export const motorIN2 = new Gpio(24,'out');
export const motorIN3 = new Gpio(17,'out');
export const motorIN4 = new Gpio(18,'out');
export const motorENB = new Gpio(27,'out');
