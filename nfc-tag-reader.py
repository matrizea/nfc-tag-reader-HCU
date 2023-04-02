#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nfc モジュールのインポート
import nfc

# サービスコードの設定
service_code = 0x1A8B

# タグとの接続時に呼び出される関数
def connected(tag):
    # Felica カードの IDm と PMm を取得
    idm, pmm = tag.polling(system_code=0xfe00)
    # タグオブジェクトの idm、pmm、sys 属性を設定
    tag.idm, tag.pmm, tag.sys = idm, pmm, 0xfe00

    # Type3Tag の場合
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            # サービスコード、ブロックコードを設定して読み取り
            sc = nfc.tag.tt3.ServiceCode(service_code >> 6 ,service_code & 0x3f)
            bc0 = nfc.tag.tt3.BlockCode(0,service=0)
            bc1 = nfc.tag.tt3.BlockCode(1,service=0)
            data0 = tag.read_without_encryption([sc],[bc0])
            data1 = tag.read_without_encryption([sc],[bc1])
            
            # 読み取ったデータを出力
            print(data0[4:11].decode("shift-jis").rstrip("\x00"))
            print(data1.decode("shift-jis").rstrip("\x00"))
        except Exception as err:
            # エラーが発生した場合は、エラーメッセージを出力
            print(("error: %s" % err))
    else:
        # Type3Tag でない場合は、エラーメッセージを出力
        print("error: tag isn't Type3Tag")

# USB 接続されたリーダーに接続して、カードを読み取る
clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
