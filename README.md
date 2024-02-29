<div align="center">
    <img width="100" alt="image" src="https://github.com/KIM2C1/MPPT/assets/76949032/aa70cd4d-f942-41c7-b457-6e8c62b95bd1" style="margin-right: 40px;">
    <img width="91" alt="image" src="https://github.com/KIM2C1/MPPT/assets/76949032/983b45ce-fcdf-4307-85a4-49ac7bc79dab">
</div>

<div align="center">
    <h1>  ⚡MPPT Management Application(진행중)⚡ </h1>
</div>

## ✒️ : 목차
- ✍️ [프로젝트 개요](#프로젝트-개요)
- 🔍 [동작영상](#-동작영상)
- 🛠 [기능(실험)](#-기능)


## 프로젝트 개요

- 캠핑카와 같은 자동차의 에너지 관리는 중요한 요소 중 하나입니다. 특히 태양광 및 알터네이터와 같은 다양한 에너지 소스를 효과적으로 활용하는 것이 필수적입니다.
- 에너지 소스들의 전압, 전류, 전력 등의 파라미터를 실시간으로 모니터링하고 최적화하는 어플리케이션을 개발하는 것을 목표로 합니다.
- 어플리케이션을 통해 사용자는 자동차의 에너지 사용 상태를 더욱 스마트하게 관리하며, 효율적인 에너지 사용으로 긴 여행을 더욱 안정적으로 준비할 수 있게 됩니다.


## **🔍 동작영상**

<details>
    <summary><h3>DEU MPPT(23-10-03)</summary>
    <div align="center">
        <img src="https://github.com/rkdaudgus94/Auto-driving-robot-vision-/assets/76949032/9d71493d-adea-4f45-b89b-780bc131ca40">
    </div>
</details>


## **🛠 기능**

### 아두이노 HC06을 통한 Bluetooth 연결 (데이터 송수신 실험)
<div align="left">
        <img width="250" src="https://github.com/KIM2C1/MPPT/assets/76949032/8404c6e0-9e5a-4e79-9d32-c94edb51b7d5">
</div>

### MPPT로부터 받은 데이터[200]
```
[69, 84, 48, 48, 48, 48, 49, 189, 50, 50, 49, 55, 53, 57, 57, 50, 50, 49, 55, 53, 57, 57, 48, 48, 54, 53, 48, 48, 48, 48, 48, 48, 49, 53, 53, 48, 48, 51, 57, 48, 48, 48, 48, 48, 48, 54, 56, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 8, 206, 0, 0, 0, 0, 2, 87, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 8, 207, 0, 0, 0, 0, 2, 87, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 8, 209, 0, 0, 0, 0, 2, 87, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 8, 210, 0, 0, 0, 0, 2, 88, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90, 13, 10]

```

- Index[0-6] : ET00001
- Index[8-11] : grid_vol, V
- Index[12-14] : grid_freq, Hz
- Index[15-18] : ac_out_vol, V
- Index[19-21] : ac_out_freq, Hz
- Index[22-25] : ac_out_app_pow
- Index[26-29] : ac_out_act_pow
- Index[30-32] : out_load_percent
- Index[33-35] : batt_vol
- Index[36-38] : batt_charge_cur
- Index[39-43] : batt_discharge_cur
- Index[44-46] : batt_capacity
- Index[47-50] : pv_in_cur
- Index[51-54] : pv_in_vol
- Index[55-59] : pv_charge_power
- Index[61-62] : Raw voltage in 0.1V
- Index[63-66] : Raw current in 0.001A
- Index[67-68] : Raw Frequency in 0.1Hz
- Index[69-72] : Raw power in 0.1W
- Index[73-76] : Raw Energy in 1Wh
- Index[77-78] : Raw pf in 0.01
- Index[79-80] : Raw alarm value
- Index[81-196] : Index[61~80]까지 반복
- Index[197] : checkSum
- Index[198] : '\r'
- Index[199] : '\n'

```dart
str result += String.fromCharCodes(strchar); // Index[0-60] ASCII로 해석
int byteintTen = 10 * decodeBytedata.getInt8(60+i); // Index[61-196] 1바이트 디코드(10의 자리)
int byteintOne = decodeBytedata.getInt8(61+i); // Index[61-196] 1바이트 디코드(1의 자리)
int byteint = byteintTen + byteintOne;
float bytefloat = byteint / 10; // 소수일 경우
```


### 실시간 그래프 기능(전압, 전류, 전력, 배터리 용량)
```dart
class GraphTile extends StatelessWidget {
  const GraphTile({
    required this.tiltle,
    super.key,
  });

  final String tiltle;

  @override
  Widget build(BuildContext context) {
    final screenSize = MediaQuery.of(context).size;

    return Container(
      padding: const EdgeInsets.all(10),
      height: 265,
      //width: 340,
      width: screenSize.width * 0.9,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.4),
            blurRadius: 5.0,
            spreadRadius: 0.0,
            offset: const Offset(0, 3),
          )
        ],
      ),
      child: Column(
        children: [
          Row(
            children: [
              Text(
                tiltle,
                style: const TextStyle(
                  //fontSize: 15,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          SizedBox(
            height: 200,
            width: screenSize.width * 0.8,
            child: const LineChartSample10(),
          ),
        ],
      ),
    );
  }
}
```
