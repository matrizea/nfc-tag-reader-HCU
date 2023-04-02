#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nfc

# NFCタグとの接続時に呼ばれる関数
def connected(tag):
    # NFCタグのIDm、PMM、SYSを出力
    print(tag)

    # Type3Tagの場合は、内容を16進数でダンプする
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            print(('  ' + '\n  '.join(tag.dump())))
        except Exception as e:
            # エラーが発生した場合は、エラーメッセージを出力
            print(f"Error: {e}")
    else:
        # Type3Tag でない場合は、エラーメッセージを出力
        print("Error: tag isn't Type3Tag")

# USB接続されたリーダーを開いて待機する
clf = nfc.ContactlessFrontend('usb')
# NFCタグが読み取られたときに connected() 関数を呼び出すように設定
clf.connect(rdwr={'on-connect': connected})
