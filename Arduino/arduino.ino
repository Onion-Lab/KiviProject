#include <SoftwareSerial.h> //시리얼통신 라이브러리 호출
#include <MsTimer2.h>

// 블루투스 시리얼 설정 
int BLUETOOTH_TX=2;
int BLUETOOTH_RX=3;

// 리니어모터 설정
int LI_MOTOR_DIR1=10;
int LI_MOTOR_DIR2=9;

// DC모터 설정
int DC_MOTOR_DIR1=5;
int DC_MOTOR_DIR2=6;

// BT로 수신된 메세지를 저장
byte buffer[1024];
int bufferPosition=0;

// 리니어모터가 한번 수행시 동작할 시간을 정의. 
// 모터의 동작 시간을 바꾸려면 아래 변수를 바꾸세요
const int LINEAR_MOTOR_OPERATION_TIME_MS = 2000;

// 블루투스 통신을 위한 객체선언
SoftwareSerial bluetoothSerial(BLUETOOTH_TX, BLUETOOTH_RX); 

// 리니어모터 상승
void liMotorUp(int operationTimeMs)
{
    digitalWrite(LI_MOTOR_DIR1, LOW);
    digitalWrite(LI_MOTOR_DIR2, HIGH);
    MsTimer2::stop();
    MsTimer2::set(operationTimeMs, liMotorInterruptFunction);
    MsTimer2::start();
}

// 리니어모터 하강
void liMotorDown(int operationTimeMs)
{
    digitalWrite(LI_MOTOR_DIR1, HIGH);
    digitalWrite(LI_MOTOR_DIR2, LOW);
    MsTimer2::stop();
    MsTimer2::set(operationTimeMs, liMotorInterruptFunction);
    MsTimer2::start();
}

// 리니어모터 정지
void liMotorStop()
{
    digitalWrite(LI_MOTOR_DIR1, LOW);
    digitalWrite(LI_MOTOR_DIR2, LOW);
}

// DC모터를 지정된 PWM으로 돌리기
void dcMotorRun(int pwm)
{
    digitalWrite(DC_MOTOR_DIR1, 0);
    analogWrite(DC_MOTOR_DIR2, pwm);
}

// DC모터 멈추기
void dcMotorStop()
{
    digitalWrite(DC_MOTOR_DIR1, LOW);
    digitalWrite(DC_MOTOR_DIR2, LOW);
}

// 아두이노가 부팅되고 최초로 호출되는 함수
void setup() 
{
    Serial.begin(9600);   // 시리얼모니터
    bluetoothSerial.begin(9600); // 블루투스 시리얼
    Serial.println("Arduino Start!\n");
    pinMode(LI_MOTOR_DIR1, OUTPUT);
    pinMode(LI_MOTOR_DIR2, OUTPUT);
    pinMode(DC_MOTOR_DIR1, OUTPUT);
    pinMode(DC_MOTOR_DIR2, OUTPUT);
    Serial.println("GPIO Initialized!\n");
}

// 메인루프
void loop()
{
    byte data;

    if (bluetoothSerial.available())
    {
        while(1)
        {
            data = bluetoothSerial.read();
            Serial.println(data);
            buffer[bufferPosition] = data;
            bufferPosition++;
            if(data == '\n')
            {
                buffer[bufferPosition] = '\0';
                bufferPosition = 0;
                Serial.write(buffer[0]);
                Serial.write(buffer[1]);
                break;
            }
        }

        switch(buffer[0])
        {
            // Linear Motor
            case 'V':
                if(buffer[1])
                {
                    liMotorUp(LINEAR_MOTOR_OPERATION_TIME_MS);
                    Serial.println("Linear Motor Up!");
                }
                else
                {
                    liMotorDown(LINEAR_MOTOR_OPERATION_TIME_MS);
                    Serial.println("Linear Motor Down!");
                }
                break;


            // DC Motor
            case 'D':
                if(buffer[1] > 0)
                {
                    dcMotorRun(buffer[1]);
                    Serial.println("DC Motor Run!");
                }
                else
                {
                    dcMotorStop();
                    Serial.println("DC Motor Stop!");
                }
                break;

            default:
                break;
        }
    }
}

void liMotorInterruptFunction()
{
    liMotorStop();
}
