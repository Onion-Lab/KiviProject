from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty
from jnius import autoclass
import Fruits

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

def getSocketStream(name):
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    socket = None
    for device in paired_devices:
        if device.getName() == name:
            socket = device.createRfcommSocketToServiceRecord(
                UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            recv_stream = socket.getInputStream()
            send_stream = socket.getOutputStream() 
            break
    socket.connect()
    return recv_stream, send_stream


class FirstApp(App):
    def __init__(self, **kwargs):
        super(FirstApp, self).__init__(**kwargs)
        self.recv_stream, self.send_stream = getSocketStream('HC-05')

    def classify_image11(self):
        img_path = self.root.ids["img11"].source

        img_features = Fruits.extract_features(img_path)

        predicted_class11 = Fruits.predict_output("weighttss.npy", img_features, activation="sigmoid")

        self.root.ids["label11"].text = "Predicted Class : " + predicted_class11

        if str(predicted_class11) == "jjampong":
            self.root.ids["_calorie1"].text = '688'
        elif str(predicted_class11) == "salad":
            self.root.ids["_calorie1"].text = '254'
        elif str(predicted_class11) == "toast":
            self.root.ids["_calorie1"].text = '381'
        else:
            self.root.ids["_calorie1"].text = '128'


    def classify_image22(self):
        img_path = self.root.ids["img22"].source

        img_features = Fruits.extract_features(img_path)

        predicted_class22 = Fruits.predict_output("weighttss.npy", img_features, activation="sigmoid")

        self.root.ids["label22"].text = "Predicted Class : " + predicted_class22

        if str(predicted_class22) == "jjampong":
            self.root.ids["_calorie2"].text = '764'
        elif str(predicted_class22) == "salad":
            self.root.ids["_calorie2"].text = '201'
        elif str(predicted_class22) == "toast":
            self.root.ids["_calorie2"].text = '420'
        else:
            self.root.ids["_calorie2"].text = '128'

    def classify_image33(self):
        img_path = self.root.ids["img33"].source

        img_features = Fruits.extract_features(img_path)

        predicted_class33 = Fruits.predict_output("weighttss.npy", img_features, activation="sigmoid")

        self.root.ids["label33"].text = "Predicted Class : " + predicted_class33

        if str(predicted_class33) == "jjampong":
            self.root.ids["_calorie3"].text = '688'
        elif str(predicted_class33) == "salad":
            self.root.ids["_calorie3"].text = '254'
        elif str(predicted_class33) == "toast":
            self.root.ids["_calorie3"].text = '381'
        else:
            self.root.ids["_calorie3"].text = '128'


    def image_select(self, filename):
        self.root.ids.img11.source = filename[0]
        pass

    def image_select1(self, filename):
        self.root.ids.img22.source = filename[0]
        pass

    def image_select2(self, filename):
        self.root.ids.img33.source = filename[0]
        pass


    def calculateWomanBMI(self, weight, height, age):
        if(weight != '' and height != '' and age!= ''):
            return str(float(66.47)+(float(13.75)*float(weight)) + (float(5)*float(height))-float(6.76)*float(age))
        else:
            return 'Error!'

    def calculateManBMI(self, weight, height, age):
        if(weight != '' and height != '' and age!= ''):
            return str(float(665.1)+(float(9.56)*float(weight)) + (float(1.85)*float(height))-float(4.68)*float(age))
        else:
            return 'Error!'

    def bluetoothSend(self, cmd, value):
        # cmd : DC모터인 경우 'D', Linear모터인 경우 'V' 입력
        # value : DC모터인 경우 pwm값, Linear모터인 경우 방향. 1:상승, 0:하강
        if self.send_stream!=None:
            self.send_stream.write(cmd.encode('utf-8') + bytes([value]) + b'\n')
            self.send_stream.flush()

class LoadDialog:
    pass

if __name__ == "__main__":
    firstApp = FirstApp(title="Fruits 360 Recognition.")
    firstApp.run()



