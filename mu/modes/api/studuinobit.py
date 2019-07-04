"""
Contains definitions for the MicroPython micro:bit related APIs so they can be
used in the editor for autocomplete and call tips.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# ここでのAPIの説明は英語だが、まずは日本語で対応する
SB_APIS = [
    # Pushbutton
    _("pystubit.board.button_a.is_pressed() \nボタンAが押されている場合Trueを返します。"),
    _("pystubit.board.button_a.was_pressed() \nボタンAが過去に押されたらTrueを返します。\nコールされたら状態をリセットします。"),
    _("pystubit.board.button_a.get_presses() \nボタンAが押された回数を返します。\nコールされたら回数をゼロにリセットします。"),
    _("pystubit.board.button_a.get_value() \nボタンAが押されている場合0を、押されていない場合1を返します。"),
    _("pystubit.board.button_b.is_pressed() \nボタンBが押されている場合Trueを返します。"),
    _("pystubit.board.button_b.was_pressed() \nボタンBが過去に押されたらTrueを返します。\nコールされたら状態をリセットします。"),
    _("pystubit.board.button_b.get_presses() \nボタンBが押された回数を返します。\nコールされたら回数をゼロにリセットします。"),
    _("pystubit.board.button_b.get_value() \nボタンBが押されている場合0を、押されていない場合1を返します。"),
    # Display 5x5 LED grid
    _("pystubit.board.display.get_pixel(x, y) \nLEDディスプレイの(x, y)にあるLEDの色を返します。戻り値の型はタプルで(R,G,B)です。"),
    _("pystubit.board.display.set_pixel(x, y, color) \nLEDディスプレイの(x,y)にあるLEDの色をcolorで設定します。\ncolorは、タプル(R,G,B), リスト[R,G,B], 整数で指定します。"),
    _("pystubit.board.display.clear() \nすべての LED の明るさを 0 (オフ)に設定します。"),
    _("""pystubit.board.display.show(x, delay=400, wait=True, loop=False, clear=False)
文字列またはイメージ'x'をLEDディスプレイに表示する場合、show(x)と記述します。'x'がイメージのリストの場合、アニメーションになります。
'delay'引数には、ミリ秒単位でフレームチェンジの速さを定義します。
'wait'引数にFalseを設定した場合、バックグラウンドでアニメーション処理されます。
'loop'引数にTrueを設定した場合、アニメーションが無限に繰り返されます。
'clear'引数にTrueを設定した場合、アニメーション終了時にディスプレイをクリアします。"""),
    _("""pystubit.board.display.scroll(string, delay=150, wait=True, loop=False)
文字列をLEDディスプレイにスクロール表示する場合、scroll(string)と記述します。
'delay'引数には、文字のスクロールする速さを定義します。
'wait'引数にFalseを設定した場合、バックグラウンドでスクロール表示処理されます。
'loop'引数にTrueを設定した場合、スクロール表示が無限に繰り返されます。"""),
    _("pystubit.board.display.on() \nディスプレイを有効にします。"),
    _("pystubit.board.display.off() \nディスプレイを無効にします。(ディスプレイに関連づけられた GPIO 端子を他の目的に再利用できるようになります)。"),
    _("pystubit.board.display.is_on() \nディスプレイが有効であれば True 、無効であれば False を返します。"),
    _("pystubit.board.display.BLACK"),
    _("pystubit.board.display.WHITE"),
    _("pystubit.board.display.RED"),
    _("pystubit.board.display.LIME"),
    _("pystubit.board.display.BLUE"),
    _("pystubit.board.display.YELLOW"),
    _("pystubit.board.display.CYAN"),
    _("pystubit.board.display.MAGENTA"),
    _("pystubit.board.display.SILVER"),
    _("pystubit.board.display.GRAY"),
    _("pystubit.board.display.MAROON"),
    _("pystubit.board.display.OLIVE"),
    _("pystubit.board.display.GREEN"),
    _("pystubit.board.display.PURPLE"),
    _("pystubit.board.display.TEAL"),
    _("pystubit.board.display.NAVY"),
    # Image
    _("""pystubit.board.Image(string, color) \n
LEDディスプレイで表示するイメージを作成します。
string引数には、'0':OFF, '1':ONでパターンを設定します。
color引数には、イメージの色を設定します。タプル(R,G,B)で指定します。
次のように記述することで、緑色のハートのイメージを作成できます。
Image('01100:10010:11110:10010:10010:', color=(0,10,0))"""),
    _("pystubit.board.Image.width() \nイメージの幅（列の数）を返します。"),
    _("pystubit.board.Image.height() \nイメージの高さ（行の数）を返します。"),
    _("pystubit.board.Image.set_pixel(x, y, value) \nイメージの(x,y)のピクセルを'value'で設定します。value引数は 0(OFF) / 1(ON)で指定します。"),
    _("pystubit.board.Image.set_pixel_color(x, y, color) \nイメージの(x,y)のピクセルの色を'color'で設定します。colorは、タプル(R,G,B), リスト[R,G,B], 整数で指定します。"),
    _("pystubit.board.Image.get_pixel(x, y) \nイメージの(x, y)のピクセルON(1)/OFF(0)を返します。"),
    _("pystubit.board.Image.get_pixel_color(x, y, hex=False) \nイメージの(x, y)のピクセルの色をピクセル色（R,G,B）を返します。\nhex引数にTrueを指定した場合、整数で色を返します。"),
    _("pystubit.board.Image.set_base_color(color) \nイメージの全ピクセルの色をcolorで設定します。colorは、タプル(R,G,B), リスト[R,G,B], 整数で指定します。"),
    _("pystubit.board.Image.shift_left(n) \nイメージをn列だけ左にシフトした新しいイメージを返します。"),
    _("pystubit.board.Image.shift_right(n) \nイメージをn列だけ右にシフトした新しいイメージを返します。"),
    _("pystubit.board.Image.shift_up(n) \nイメージをn行だけ上にシフトした新しいイメージを返します。"),
    _("pystubit.board.Image.shift_down(n) \nイメージをn行だけ下にシフトした新しいイメージを返します。"),
    _("pystubit.board.Image.copy() \nイメージのコピーを返します。"),
    _("pystubit.board.Image.HEART"),
    _("pystubit.board.Image.HEART_SMALL"),
    _("pystubit.board.Image.HAPPY"),
    _("pystubit.board.Image.SMILE"),
    _("pystubit.board.Image.SAD"),
    _("pystubit.board.Image.CONFUSED"),
    _("pystubit.board.Image.ANGRY"),
    _("pystubit.board.Image.ASLEEP"),
    _("pystubit.board.Image.SURPRISED"),
    _("pystubit.board.Image.SILLY"),
    _("pystubit.board.Image.FABULOUS"),
    _("pystubit.board.Image.MEH"),
    _("pystubit.board.Image.YES"),
    _("pystubit.board.Image.NO"),
    _("pystubit.board.Image.CLOCK12"),
    _("pystubit.board.Image.CLOCK11"),
    _("pystubit.board.Image.CLOCK10"),
    _("pystubit.board.Image.CLOCK9"),
    _("pystubit.board.Image.CLOCK8"),
    _("pystubit.board.Image.CLOCK7"),
    _("pystubit.board.Image.CLOCK6"),
    _("pystubit.board.Image.CLOCK5"),
    _("pystubit.board.Image.CLOCK4"),
    _("pystubit.board.Image.CLOCK3"),
    _("pystubit.board.Image.CLOCK2"),
    _("pystubit.board.Image.CLOCK1"),
    _("pystubit.board.Image.ARROW_N"),
    _("pystubit.board.Image.ARROW_NE"),
    _("pystubit.board.Image.ARROW_E"),
    _("pystubit.board.Image.ARROW_SE"),
    _("pystubit.board.Image.ARROW_S"),
    _("pystubit.board.Image.ARROW_SW"),
    _("pystubit.board.Image.ARROW_W"),
    _("pystubit.board.Image.ARROW_NW"),
    _("pystubit.board.Image.TRIANGLE"),
    _("pystubit.board.Image.TRIANGLE_LEFT"),
    _("pystubit.board.Image.CHESSBOARD"),
    _("pystubit.board.Image.DIAMOND"),
    _("pystubit.board.Image.DIAMOND_SMALL"),
    _("pystubit.board.Image.SQUARE"),
    _("pystubit.board.Image.SQUARE_SMALL"),
    _("pystubit.board.Image.RABBIT"),
    _("pystubit.board.Image.COW"),
    _("pystubit.board.Image.MUSIC_CROTCHET"),
    _("pystubit.board.Image.MUSIC_QUAVER"),
    _("pystubit.board.Image.MUSIC_QUAVERS"),
    _("pystubit.board.Image.PITCHFORK"),
    _("pystubit.board.Image.XMAS"),
    _("pystubit.board.Image.PACMAN"),
    _("pystubit.board.Image.TARGET"),
    _("pystubit.board.Image.TSHIRT"),
    _("pystubit.board.Image.ROLLERSKATE"),
    _("pystubit.board.Image.DUCK"),
    _("pystubit.board.Image.HOUSE"),
    _("pystubit.board.Image.TORTOISE"),
    _("pystubit.board.Image.BUTTERFLY"),
    _("pystubit.board.Image.STICKFIGURE"),
    _("pystubit.board.Image.GHOST"),
    _("pystubit.board.Image.SWORD"),
    _("pystubit.board.Image.GIRAFFE"),
    _("pystubit.board.Image.SKULL"),
    _("pystubit.board.Image.UMBRELLA"),
    _("pystubit.board.Image.SNAKE"),
    _("pystubit.board.Image.ALL_CLOCKS"),
    _("pystubit.board.Image.ALL_ARROWS"),
    _("pystubit.board.Image.BLACK"),
    _("pystubit.board.Image.WHITE"),
    _("pystubit.board.Image.RED"),
    _("pystubit.board.Image.LIME"),
    _("pystubit.board.Image.BLUE"),
    _("pystubit.board.Image.YELLOW"),
    _("pystubit.board.Image.CYAN"),
    _("pystubit.board.Image.MAGENTA"),
    _("pystubit.board.Image.SILVER"),
    _("pystubit.board.Image.GRAY"),
    _("pystubit.board.Image.MAROON"),
    _("pystubit.board.Image.OLIVE"),
    _("pystubit.board.Image.GREEN"),
    _("pystubit.board.Image.PURPLE"),
    _("pystubit.board.Image.TEAL"),
    _("pystubit.board.Image.NAVY"),
    # buzzer
    _("""pystubit.board.buzzer.on(sound, duration=-1)
ブザーから指定された高さの音を出力します。
sound引数には、文字列で'C3'～'G9'のコード、'48'～'127'のMIDIノートナンバー、整数で周波数を設定します。
duration引数に正の整数を設定した場合、設定した値（ミリ秒単位）の間、音を出力します。"""),
    _("pystubit.board.buzzer.off() \n 音が出力されている場合、停止します。"),
    # temperature
    _("pystubit.board.temperature.get_value() \n 基板上の温度センサーの値（0-4095）を返します。"),
    _("pystubit.board.temperature.get_celsius() \n 基板上の温度センサーの値を温度（セ氏）を返します。"),
    # lightsensor
    _("pystubit.board.lightsensor.get_celsius() \n 基板上の光センサーの値（0-4095）を返します。"),
    # accelerometer
    _("pystubit.board.accelerometer.get_x() \n x軸の加速度を返します。戻り値の型は符号付整数、デフォルトの単位はメートル/秒/秒です。"),
    _("pystubit.board.accelerometer.get_y() \n y軸の加速度を返します。戻り値の型は符号付整数、デフォルトの単位はメートル/秒/秒です。"),
    _("pystubit.board.accelerometer.get_z() \n z軸の加速度を返します。戻り値の型は符号付整数、デフォルトの単位はメートル/秒/秒です。"),
    _("pystubit.board.accelerometer.get_values() \n x,y,z軸の加速度をタプルで返します。(get_x(), get_y(), get_z())。"),
    _("pystubit.board.accelerometer.set_fs(value) \n センサーのフルスケールを設定します。\n2G～16Gまで計測可能で、value引数には、文字列で'2g'/'4g'/'8g'/'16g'を設定します。"),
    _("pystubit.board.accelerometer.set_sf(value) \n センサーのスケールファクタを設定します。\nミリGまたはメートル/秒/秒の単位が指定できます。value引数には、文字列で'mg'/'ms2'を設定します。"),
    # gyro
    _("pystubit.board.gyro.get_x() \n x軸の角速度を返します。戻り値の型は符号付整数、デフォルトの単位は角度/秒です。"),
    _("pystubit.board.gyro.get_y() \n y軸の角速度を返します。戻り値の型は符号付整数、デフォルトの単位は角度/秒です。"),
    _("pystubit.board.gyro.get_z() \n z軸の角速度を返します。戻り値の型は符号付整数、デフォルトの単位は角度/秒です。"),
    _("pystubit.board.gyro.get_values() \n x,y,z軸の角速度をタプルで返します。(get_x(), get_y(), get_z())。"),
    _("pystubit.board.gyro.set_fs(value) \n センサーのフルスケールを設定します。\n250度/秒～2000度/秒まで計測可能で、value引数には、文字列で'250dps'/'500dps'/'1000dps'/'2000dps'を設定します。"),
    _("pystubit.board.gyro.set_sf(value) \n センサーのスケールファクタを設定します。\n角度/秒またはラジアン/秒の単位が指定できます。value引数には、文字列で'dps'/'rps'を設定します。"),
    # compass
    _("pystubit.board.compass.get_x() \n x軸の磁場を返します。戻り値の型は符号付整数、デフォルトの単位はマイクロ・テスラです。\nN極が近づくと+, S極が近づくと-になります。"),
    _("pystubit.board.compass.get_y() \n y軸の磁場を返します。戻り値の型は符号付整数、デフォルトの単位はマイクロ・テスラです。\nN極が近づくと+, S極が近づくと-になります。"),
    _("pystubit.board.compass.get_z() \n z軸の磁場を返します。戻り値の型は符号付整数、デフォルトの単位はマイクロ・テスラです。\nN極が近づくと+, S極が近づくと-になります。"),
    _("pystubit.board.compass.get_values() \n x,y,z軸の磁場をタプルで返します。(get_x(), get_y(), get_z())。"),
    _("pystubit.board.compass.calibrate() \n 磁気センサーのキャリブレーションを開始します。LEDディスプレイ上に円を描くようデバイスを回転させます。"),
    _("pystubit.board.compass.is_calibrated() \n キャリブレーションが成功したかどうかにより True または False を返します。"),
    _("pystubit.board.compass.clear_calibration() \n キャリブレーションを取り消します。"),
    _("pystubit.board.compass.heading() \n 磁針の向きを返します。0～360°の整数で、時計回りで北が180°になります。"),
    # p0
    _("pystubit.board.p0.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p0.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p0.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p0.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p0.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p0.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p0.status()\n PWMの使用状況をREPLに表示します。"),
    _("pystubit.board.p0.read_analog(mv=False)\n 端子からアナログ信号をリードします。\n mv=Falseの場合、0 (0V の意味）から 4095 (3.3V の意味)までの間の整数を返します。mv=Trueの場合、電圧をmV（ミリ・ボルト）で返します。"),
    # p1
    _("pystubit.board.p1.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p1.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p1.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p1.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p1.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p1.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p1.status()\n PWMの使用状況をREPLに表示します。"),
    _("pystubit.board.p1.read_analog(mv=False)\n 端子からアナログ信号をリードします。\n mv=Falseの場合、0 (0V の意味）から 4095 (3.3V の意味)までの間の整数を返します。mv=Trueの場合、電圧をmV（ミリ・ボルト）で返します。"),
    # p2
    _("pystubit.board.p2.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p2.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p2.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p2.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p2.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p2.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p2.status()\n PWMの使用状況をREPLに表示します。"),
    _("pystubit.board.p2.read_analog(mv=False)\n 端子からアナログ信号をリードします。\n mv=Falseの場合、0 (0V の意味）から 4095 (3.3V の意味)までの間の整数を返します。mv=Trueの場合、電圧をmV（ミリ・ボルト）で返します。"),
    # p3
    _("pystubit.board.p3.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p3.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p3.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p3.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p3.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p3.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p3.status()\n PWMの使用状況をREPLに表示します。"),
    _("pystubit.board.p3.read_analog(mv=False)\n 端子からアナログ信号をリードします。\n mv=Falseの場合、0 (0V の意味）から 4095 (3.3V の意味)までの間の整数を返します。mv=Trueの場合、電圧をmV（ミリ・ボルト）で返します。"),
    # p4
    _("pystubit.board.p4.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p4.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p4.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p4.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p4.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p4.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p4.status()\n PWMの使用状況をREPLに表示します。"),
    # p5
    _("pystubit.board.p5.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p5.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p5.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p5.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p5.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p5.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p5.status()\n PWMの使用状況をREPLに表示します。"),
    _("pystubit.board.p5.read_analog(mv=False)\n 端子からアナログ信号をリードします。\n mv=Falseの場合、0 (0V の意味）から 4095 (3.3V の意味)までの間の整数を返します。mv=Trueの場合、電圧をmV（ミリ・ボルト）で返します。"),
    # p6
    _("pystubit.board.p6.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p6.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p6.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p6.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p6.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p6.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p6.status()\n PWMの使用状況をREPLに表示します。"),
    # p7
    _("pystubit.board.p7.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p7.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p7.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p7.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p7.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p7.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p7.status()\n PWMの使用状況をREPLに表示します。"),
    # p8
    _("pystubit.board.p8.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p8.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p8.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p8.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p8.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p8.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p8.status()\n PWMの使用状況をREPLに表示します。"),
    _("pystubit.board.p8.read_analog(mv=False)\n 端子からアナログ信号をリードします。\n mv=Falseの場合、0 (0V の意味）から 4095 (3.3V の意味)までの間の整数を返します。mv=Trueの場合、電圧をmV（ミリ・ボルト）で返します。"),
    # p9
    _("pystubit.board.p9.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p9.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p9.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p9.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p9.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p9.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p9.status()\n PWMの使用状況をREPLに表示します。"),
    _("pystubit.board.p9.read_analog(mv=False)\n 端子からアナログ信号をリードします。\n mv=Falseの場合、0 (0V の意味）から 4095 (3.3V の意味)までの間の整数を返します。mv=Trueの場合、電圧をmV（ミリ・ボルト）で返します。"),
    # p10
    _("pystubit.board.p10.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p10.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p10.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p10.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p10.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p10.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p10.status()\n PWMの使用状況をREPLに表示します。"),
    # p11
    _("pystubit.board.p11.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p11.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p11.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p11.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p11.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p11.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p11.status()\n PWMの使用状況をREPLに表示します。"),
    # p12
    _("pystubit.board.p12.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p12.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p12.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p12.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p12.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p12.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p12.status()\n PWMの使用状況をREPLに表示します。"),
    # p13
    _("pystubit.board.p13.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p13.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p13.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p13.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p13.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p13.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p13.status()\n PWMの使用状況をREPLに表示します。"),
    # p14
    _("pystubit.board.p14.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p14.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p14.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p14.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p14.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p14.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p14.status()\n PWMの使用状況をREPLに表示します。"),
    # p15
    _("pystubit.board.p15.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p15.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p15.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p15.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p15.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p15.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p15.status()\n PWMの使用状況をREPLに表示します。"),
    # p16
    _("pystubit.board.p16.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p16.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p16.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p16.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p16.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p16.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p16.status()\n PWMの使用状況をREPLに表示します。"),
    _("pystubit.board.p16.read_analog(mv=False)\n 端子からアナログ信号をリードします。\n mv=Falseの場合、0 (0V の意味）から 4095 (3.3V の意味)までの間の整数を返します。mv=Trueの場合、電圧をmV（ミリ・ボルト）で返します。"),
    # p19
    _("pystubit.board.p19.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p19.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p19.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p19.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p19.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p19.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p19.status()\n PWMの使用状況をREPLに表示します。"),
    # p20
    _("pystubit.board.p20.write_digital(value)\n 端子からデジタル出力します。\n value引数が1の場合はハイに設定し、0の場合はローに設定します。"),
    _("pystubit.board.p20.read_digital()\n 端子からデジタル信号をリードします。\n 戻り値は、ハイの場合は1、ローの場合は0を返します。"),
    _("pystubit.board.p20.write_analog(value)\n PWM信号を端子に出力します。\n value引数は、浮動小数点数で、0(0%)～100(100%)を設定します。"),
    _("pystubit.board.p20.set_analog_period(period, timer=-1)\n PWM 信号の周期を period にミリ秒単位で設定します。有効な最小値は 1ms です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p20.set_analog_period_microseconds(period, timer=-1)\n PWM 信号の周期を period にマイクロ秒単位で設定します。有効な最小値は 256μs です。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p20.set_analog_hz(hz, timer=-1)\n PWM 信号の周期を 周波数で設定します。\n timer引数でPWMに使用するタイマーのIDを0～3で設定できます。"),
    _("pystubit.board.p20.status()\n PWMの使用状況をREPLに表示します。"),
    # DC Motor
    _("pyatcrobo2.parts.DCMotor(pin)\n DCモーターのインスタンスを生成します。\n pin引数にDCモーターを接続しているピンを文字列（'M1'/ 'M2'）で指定します。"),
    _("pyatcrobo2.parts.DCMotor.cw()\n DCモーターを正転で回転します。"),
    _("pyatcrobo2.parts.DCMotor.ccw()\n DCモーターを逆転で回転します。"),
    _("pyatcrobo2.parts.DCMotor.stop()\n DCモーターの回転を脱力で停止します。"),
    _("pyatcrobo2.parts.DCMotor.brake()\n DCモーターを回転を停止します。"),
    _("pyatcrobo2.parts.DCMotor.power(power)\n DCモーターのパワーを設定します。\n power引数には、0～255の整数を設定します。"),
    # Servomotor
    _("pyatcrobo2.parts.Servomotor(pin)\n サーボモーターのインスタンスを生成します。\n pin引数にサーボモーターを接続しているピンを文字列（'P13'/'P14'/ 'P15'/ 'P16'）で指定します。"),
    _("pyatcrobo2.parts.Servomotor.set_angle(degree)\n サーボモーターの角度を制御します。\n degree引数に角度(0～180)を整数で設定します。"),
    # Buzzer
    _("pyatcrobo2.parts.Buzzer(pin)\n ブザーのインスタンスを生成します。\n pin引数にブザーを接続しているピンを文字列（'P13'/'P14'/ 'P15'/ 'P16'）で指定します。"),
    _("""pyatcrobo2.parts.Buzzer.on(sound, volume=-1, duration=-1)
 ブザーから指定された高さの音を出力します。
 sound引数には、文字列で'C3'～'G9'のコード、'48'～'127'のMIDIノートナンバー、整数で周波数を設定します。
 volume引数には、ボリュームを百分率（整数（0～99））で設定します。
 duration引数に正の整数を設定した場合、設定した値（ミリ秒単位）の間、音を出力します。"""),
    _("pyatcrobo2.parts.Buzzer.off() \n 音が出力されている場合、停止します。"),
    # LED
    _("pyatcrobo2.parts.LED(pin)\n LEDのインスタンスを生成します。\n pin引数にLEDを接続しているピンを文字列（'P13'/'P14'/'P15'/'P16'）で指定します。"),
    _("pyatcrobo2.parts.LED.on() \n LEDを点灯します。"),
    _("pyatcrobo2.parts.LED.off() \n LEDを消灯します。"),
    # IRPhotoReflector
    _("pyatcrobo2.parts.IRPhotoReflector(pin)\n 赤外線フォトリフレクタのインスタンスを生成します。\n pin引数に赤外線フォトリフレクタを接続しているピンを文字列（'P0'/'P1'/'P2'）で指定します。"),
    _("pyatcrobo2.parts.IRPhotoReflector.get_value() \n センサーの値(0～4095)を取得します。"),
    # LightSensor
    _("pyatcrobo2.parts.LightSensor(pin)\n 光センサーのインスタンスを生成します。\n pin引数に光センサーを接続しているピンを文字列（'P0'/'P1'/'P2'）で指定します。"),
    _("pyatcrobo2.parts.LightSensor.get_value() \n センサーの値(0～4095)を取得します。"),
    # Temperature
    _("pyatcrobo2.parts.Temperature(pin)\n 温度センサーのインスタンスを生成します。\n pin引数に温度センサーを接続しているピンを文字列（'P0'/'P1'/'P2'）で指定します。"),
    _("pyatcrobo2.parts.Temperature.get_value() \n センサーの値(0～4095)を取得します。"),
    _("pyatcrobo2.parts.Temperature.get_celsius() \n センサーの値を温度（セ氏）で取得します。"),
    # SoundSensor
    _("pyatcrobo2.parts.SoundSensor(pin)\n 音センサーのインスタンスを生成します。\n pin引数に音センサーを接続しているピンを文字列（'P0'/'P1'/'P2'）で指定します。"),
    _("pyatcrobo2.parts.SoundSensor.get_value() \n センサーの値(0～4095)を取得します。"),
    # TouchSensor
    _("pyatcrobo2.parts.TouchSensor(pin)\n タッチセンサーのインスタンスを生成します。\n pin引数にタッチセンサーを接続しているピンを文字列（'P0'/'P1'/'P2'）で指定します。"),
    _("pyatcrobo2.parts.TouchSensor.get_value() \n センサーの値(0/1)を取得します。"),
    # Accelerometer
    _("pyatcrobo2.parts.Accelerometer(pin)\n 加速度センサーのインスタンスを生成します。\n pin引数に加速度センサーを接続しているピンを文字列（'I2C'）で指定します。"),
    _("""pyatcrobo2.parts.Accelerometer.configuration(highres, scale)
 加速度センサーを設定します。
 highres引数には、高解像度指定をTrue/Falseで設定します。Trueを指定した場合、解像度は16bit、Falseを指定した場合、解像度は8bitになります。
 scale引数には、加速度の測定範囲(2G～8G)を指定します。整数で2,4,8をのいずれかを設定します。"""),
    _("pyatcrobo2.parts.Accelerometer.get_x() \n x軸の加速度を返します。戻り値の型は符号付整数、デフォルトの単位はメートル/秒/秒です。"),
    _("pyatcrobo2.parts.Accelerometer.get_y() \n y軸の加速度を返します。戻り値の型は符号付整数、デフォルトの単位はメートル/秒/秒です。"),
    _("pyatcrobo2.parts.Accelerometer.get_z() \n z軸の加速度を返します。戻り値の型は符号付整数、デフォルトの単位はメートル/秒/秒です。"),
    _("pyatcrobo2.parts.Accelerometer.get_values() \n x,y,z軸の加速度をタプルで返します。(get_x(), get_y(), get_z())。"),
    # RNG
    _("random.getrandbits(n) \nReturn an integer with n random bits."),
    _("random.seed(n) \nInitialise the random number generator with a known integer 'n'."),
    _("random.randint(a, b) \nReturn a random whole number between a and b (inclusive)."),
    _("random.randrange(stop) \nReturn a random whole number between 0 and up to (but not including) stop."),
    _("random.choice(seq) \nReturn a randomly selected element from a sequence of objects (such as a list)."),
    _("random.random() \nReturn a random floating point number between 0.0 and 1.0."),
    _("random.uniform(a, b) \nReturn a random floating point number between a and b (inclusive)."),
    # OS
    _("os.listdir() \nReturn a list of the names of all the files contained within the local\non-device file system."),
    _("os.remove(filename) \nRemove (delete) the file named filename."),
    _("os.size(filename) \nReturn the size, in bytes, of the file named filename."),
    _("os.uname() \nReturn information about MicroPython and the device."),
    _("os.getcwd() \nReturn current working directory"),
    _("os.chdir(path) \nChange current working directory"),
    _("os.mkdir(path) \nMake new directory"),
    _("os.rmdir(path) \nRemove directory"),
    _("os.listdir(path='.') \nReturn list of directory. Defaults to current working directory."),
    # SYS
    _("sys.version \nReturn Python version as a string "),
    _("sys.version_info \nReturn Python version as a tuple"),
    _("sys.implementation \nReturn MicroPython version"),
    _("sys.platform \nReturn hardware platform as string, e.g. 'esp8266' or 'esp32'"),
    _("sys.byteorder \nReturn platform endianness. 'little' for least-significant byte first or 'big' for most-significant byte first." ),
    _("sys.print_exception(ex) \nPrint to the REPL information about the exception 'ex'."),
    # Machine module
    _("machine.reset() \nResets the device in a manner similar to pushing the external RESET button"),
    _("machine.freq() \nReturns CPU frequency in hertz."),

    _("""machine.Pin(id [, mode, pull])\nCreate a Pin-object. Only id is mandatory.
mode (optional): specifies the pin mode (Pin.OUT or Pin.IN)
pull (optional): specifies if the pin has a pull resistor attached 
  pull can be one of: None, Pin.PULL_UP or Pin.PULL_DOWN."""),
    _("""machine.Pin.value([x])\n This method allows to set and get the
value of the pin, depending on whether the argument x is supplied or not.
If the argument is omitted, the method returns the actual input value (0 or 1) on the pin.
If the argument is supplied, the method sets the output to the given value."""),
    _("machine.Pin.OUT"),
    _("machine.Pin.IN"),
    _("machine.Pin.PULL_UP"),
    _("machine.Pin.PULL_DOWN"),
    _("""machine.ADC(pin)
Create an ADC object associated with the given pin. 
This allows you to then read analog values on that pin.
machine.ADC(machine.Pin(39))"""),
    _("machine.ADC.read() \nRead the analog pin value.\n\nadc = machine.ADC(machine.Pin(39))\nvalue = adc.read()"),
    # Time module
    _("time.sleep(seconds) \nSleep the given number of seconds."),
    _("time.sleep_ms(milliseconds) \nSleep the given number of milliseconds."),
    _("time.sleep_us(milliseconds) \nSleep the given number of microseconds."),
    _("time.ticks_ms() \nReturn number of milliseconds from an increasing counter. Wraps around after some value."),
    _("time.ticks_us() \nReturn number of microseconds from an increasing counter. Wraps around after some value."),
    _("time.ticks_diff() \nCompute difference between values ticks values obtained from time.ticks_ms() and time.ticks_us()."),
    _("""time.time() 
Returns the number of seconds, as an integer, since the Epoch, 
assuming that underlying RTC is set and maintained. If an
RTC is not set, this function returns number of seconds since a
port-specific reference point in time (usually since boot or reset)."""),
    # Network module
    _("""network.WLAN(interface_id) \n
Create a WLAN interface object. Supported interfaces are:
network.STA_IF (station aka client, connects to upstream WiFi access points) and 
network.AP_IF (access point mode, allows other WiFi clients to connect)."""),
    _("network.WLAN.STA_IF"),
    _("network.WLAN.AP_IF"),
    _("""network.WLAN.active([ is_active ])
Activates or deactivates the network interface when given boolean
argument. When argument is omitted the function returns the current state."""),
    _("""network.WLAN.connect(ssid, password)
Connect to the specified wireless network using the specified password."""),
    _("network.WLAN.disconnect() \nDisconnect from the currently connected wireless network."),
    _("""network.WLAN.scan()
Scan for the available wireless networks. Scanning is only possible on
STA interface. Returns list of tuples with the information about WiFi
access points:
   (ssid, bssid, channel, RSSI, authmode, hidden)"""),
    _("""network.WLAN.status()
Return the current status of the wireless connection. Possible values:
 - STAT_IDLE (no connection and no activity)
 - STAT_CONNECTING (connecting in progress)
 - STAT_WRONG_PASSWORD (failed due to incorrect password),
 - STAT_NO_AP_FOUND (failed because no access point replied),
 - STAT_CONNECT_FAIL (failed due to other problems),
 - STAT_GOT_IP (connection successful)"""),
    _("""network.WLAN.isconnected()
In case of STA mode, returns True if connected to a WiFi access point
and has a valid IP address. In AP mode returns True when a station is
connected. Returns False otherwise."""),
    _("""network.WLAN.ifconfig([ (ip, subnet, gateway, dns) ]) 
Get/set IP-level network interface parameters: IP address, subnet
mask, gateway and DNS server. When called with no arguments, this
method returns a 4-tuple with the above information. To set the above
values, pass a 4-tuple with the required information. For example:

nic = network.WLAN(network.WLAN.AP_IF)
nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))"""),
    # urequests module
    _("""urequests.get(url, headers={})
Send HTTP GET request to the given URL. 
An optional dictionary of HTTP headers can be provided.
Returns a urequests.Response-object"""),
    _("""urequests.post(url, data=None, json=None, headers={}) 
Send HTTP POST request to the given URL. Returns a
urequests.Response-object.
 - data (optional): bytes to send in the body of the request.
 - json (optional): JSON data to send in the body of the Request.
 - headers (optional): An optional dictionary of HTTP headers."""),
    _("urequests.Response() \n Object returned by "),
    _("urequests.Response.text \n String representation of response "),
    _("urequests.Response.json() \n Convert Response from JSON to Python dictionary."),
    # NeoPixel module
    _("""neopixel.NeoPixel(pin, n) 

Create a list representing a strip of 'n' neopixels controlled from
the specified pin (e.g. machine.Pin(0)). Use the resulting object to
change each pixel by position (starting from 0). Individual pixels
are given RGB (red, green, blue) values between 0-255 as a tupel. For
example, (255, 255, 255) is white:

np = neopixel.NeoPixel(machine.Pin(0), 8)\nnp[0] = (255, 0, 128)
np.write()"""),
    _("neopixel.NeoPixel.write() \nShow the pixels. Must be called for any updates to become visible."),
    # Math functions
    _("math.sqrt(x) \nReturn the square root of 'x'."),
    _("math.pow(x, y) \nReturn 'x' raised to the power 'y'."),
    _("math.exp(x) \nReturn math.e**'x'."),
    _("math.log(x, base=math.e) \nWith one argument, return the natural logarithm of 'x' (to base e).\nWith two arguments, return the logarithm of 'x' to the given 'base'."),
    _("math.cos(x) \nReturn the cosine of 'x' radians."),
    _("math.sin(x) \nReturn the sine of 'x' radians."),
    _("math.tan(x) \nReturn the tangent of 'x' radians."),
    _("math.acos(x) \nReturn the arc cosine of 'x', in radians."),
    _("math.asin(x) \nReturn the arc sine of 'x', in radians."),
    _("math.atan(x) \nReturn the arc tangent of 'x', in radians."),
    _("math.atan2(x, y) \nReturn atan(y / x), in radians."),
    _("math.ceil(x) \nReturn the ceiling of 'x', the smallest integer greater than or equal to 'x'."),
    _("math.copysign(x, y) \nReturn a float with the magnitude (absolute value) of 'x' but the sign of 'y'. "),
    _("math.fabs(x) \nReturn the absolute value of 'x'."),
    _("math.floor(x) \nReturn the floor of 'x', the largest integer less than or equal to 'x'."),
    _("math.fmod(x, y) \nReturn 'x' modulo 'y'."),
    _("math.frexp(x) \nReturn the mantissa and exponent of 'x' as the pair (m, e). "),
    _("math.ldexp(x, i) \nReturn 'x' * (2**'i')."),
    _("math.modf(x) \nReturn the fractional and integer parts of x.\nBoth results carry the sign of x and are floats."),
    _("math.isfinite(x) \nReturn True if 'x' is neither an infinity nor a NaN, and False otherwise."),
    _("math.isinf(x) \nReturn True if 'x' is a positive or negative infinity, and False otherwise."),
    _("math.isnan(x) \nReturn True if 'x' is a NaN (not a number), and False otherwise."),
    _("math.trunc(x) \nReturn the Real value 'x' truncated to an Integral (usually an integer)."),
    _("math.radians(x) \nConvert angle 'x' from degrees to radians."),
    _("math.degrees(x) \nConvert angle 'x' from radians to degrees."),
]
