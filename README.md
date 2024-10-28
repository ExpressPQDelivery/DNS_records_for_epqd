Welcome to the ExpressPQDelivery Project  
==============================  
The DNS_records_for_epqd is a DNS record(TXT, TLSA) generator for E-Box.   
Set up a DNS resolver using bind9, and put the resolver close to a client. Then, upload the DNS records to the DNS server.  
`example_zonefile.txt` is an instance of DNS records for diltihium2.  
An example of E-Box for PQC algorithms is `ebox-need_for_sign.txt`, which is located in each folder.  
We provide code to assist in 1. generating certificates, 2. creating an E-Box based on them, and dividing it into 3. TXT and 4. TLSA records.  

## Requirements  
Openssl installation including Oqsprovider. (In our work, we use v 3.2.0)  

## How to start(Linux Ubuntu)  
## 1. Generate Certificates and convert the certificate to der format.  
```bash
openssl req -x509 -new -newkey dilithium2 -keyout dil2_priv.key -out dil2_crt.pem -nodes -subj "/CN=test CA" -days 365
openssl x509 -inform PEM -outform DER -in dil2_crt.pem -out dil2_crt.der
```

## 2. Generate E-Box
### 2.1 Generate base files for TXT records  
you should enter the correct number of TXT and TLSA records.   
dilithium2: TXT 3, TLSA 4  
dilithium3: TXT 5, TLSA 6  
dilithium5: TXT 6, TLSA 7  
falcon512: TXT 1, TLSA 2  
falcon1024: TXT 2, TLSA 4  
  
(Please refer to our paper for detail)  
```bash
python3 gen_base_txt_record.py
```  
You may get `ebox-need_for_sign.txt` and `TXT_EBOX-proto.txt`.  
You need to add signature value at `TXT_EBOX-proto.txt` to use this as E-Box TXT records.  

### 2.2 Generate signature for E-Box  
we use sha256 hash value to generate signature.  
```bash
openssl sha256 dil2_crt.der
```  
then, concatate the hash value at `ebox-need_for_sign.txt`. 

```
Example)
340020240923103333202509231033330(hash value)  
```  

Generate signature with server's private key.  
```bash
openssl dgst -sha256 -sign dil2_priv.key -out sign.256 ebox-need_for_sign.txt  
```  
Encode signature in base64 format.  
```bash
openssl base64 -in sign.256 -out base64_signature
```  
Split the signature value into an appropriate size and wrap it with " ".
```bash
python3 txt_records_generator.py
``` 
Then, we get `base_output2.txt`.  

## 3. Generate TXT records for ExpressPQDelivery  
Paste the contents of `base_output2.txt` into `TXT_EBOX-proto.txt`.  Divide it into appropriate sizes (not exceeding 1,232 bytes) and upload it to the DNS resolver according to domain name conventions. Refer to our example_zonefile.txt.

## 4. Generate TLSA records for ExpressPQDelivery  

We use online TLSA record generator for get TLSA record value.  
<https://ssl-tools.net/tlsa-generator>  
Domain Issued Certificate, use full certificate, No Hash.  
we only need the value except `_443._udp.esplab.io. IN TLSA 2 0 0`  
save the TLSA value in txt file name like *dil2_tlsa.txt*  
```bash
python3 tlsa_record_new.py
```  
Then, you can get TLSA records appling _Optimized fragmentation_ for _EPQD_ named *TLSA_record_output.txt*.  

## Example records  

### A. TXT records for ExpressPQDelivery  
```
[dil2.ebox-0.esplab.io](http://dil2.ebox-0.esplab.io/). IN TXT   "3" "4" "0" "0" "20240923103333" "20250923103333" "0" "VTX1kN2+gQX3AtBAYr/4gHItDtWD+VcB6WDbbDvwHGZDDFFrk5ip1GHGeKXfY4seHssyBOTcxQw1a8OuzecVW2HIH2/EKdW81gaEoc3w//6cAgnUjaJcZRIRHVZdtB9EQ9qovGaNHjdz7" "Xxv38GOG46lHQROwb8mHTTszdfCHzlSB4uob5TB1OENA8rIuqClZ5koeSuSvM514fyfQ5xPvD1gDDg4HQjOC5iGkZcM1VjW33/9hKXp9zv96sN7IB9RyfckzDTCEWy+VZ+y7Y2h/Y72hh" "Dq3czcLe7DHSO4twgDliXTEDPfkQw4XORfwlQBYNK6e4QdyjY3NA1WFK3DOnQEED+y7KjRki+LrFUIr19TTC48PrgPyvKtwiBFDEG/l3URHBJBwPnzgI23s1ZsFUqOdKDRpJG4hOBl5U+XZFVMXy85/xEoxHkOEctTyRYKgXCyA1fZwxuhAh/G+xWCxc1YGpANH9epQgk4ioj5p3mtl2ky3N2KrlzY98cnRibs8OEJ8EGip1A8Txz0P4P/Ln275nyS8gLysmUMPW99OKx872NajjS4ydXVQR9TgI6iMsiynxrpGRD/kNJDiOMSlI3Ohh3VDWlnjpMaemdreHh7aGnObPAeZ3jVAyBPcr5SckX4DAzRVey9UaDrn+Rj/vKleYBbkWpW" "Bviu8hZD2Ha7Hv37bn+slLvdzBAAWQ8zAk3Dc+3OnLv5zG9zwDL+YLes8elGxlysnPOY8+mlZqckvvnfFMK31YOl9NwI5B4qFGPE+ad318MpOZfrXm3rCH4YOoIIanMYa0A9TfyxPrT8g"
;

[dil2.ebox-1.esplab.io](http://dil2.ebox-1.esplab.io/).  IN      TXT     "xyPKF1EBrkc8q94AiX/i4eqqbihX2QPrTpwKxt+KTg7WC3PWV5NVXXqOPQPmJLBRlzt9jbmO6RJuTwi0TCzicRKOreLW/RhYvh+q/bteZL6apjMz64HMSSyUCohHb0JitkEKaOASX24iP" "bHc3cPJLXWApB04V9F0h5WJZYPLKkHV0D2TCHEDnRi9a+ecv/W6A84nhbAj8ZqgaDUyz+08Sa7dY7U+LVrBcoj9bEoBx1v/My9Jz0TZI/RnMPDLSb6xVTmZ4BCaXqbSIEgG2LaeTSnhdd" "2vBA4EuHJKdpKW1IJiXXdpO8K/h2Yzrivo59xNESrw9Q/k45C1dnIN7eGMFH3T1qIJsdAs8gvbH180vEzrisSm2NWyh24O7a2cjaP3fL1Jya+SXkWSdNdjw4p/EOXmb/of9QFH0Kj58Vn" "xb4BUmhA4YwsUmntOCVqXn+nl7/Wmu3fRxd9WFehlYjvXD1ktde75vSyyt6xq9sNBOI1DGsVWnQXmtUn0Cdm/ZPvUMo65vaMPoc8XqhiVkT07tLlvHnNxLWhLJsZs67UsKgp2fDR28RtZ" "XayQ3TanIjm5ITlg4T840WbR/1TMcNGOU3HMONOSO+jMxkj2zuGKeWN4FQBhLlK5ltcv6A654ovlDdss9C9IyXXPynIZ69Z9nBX5M8mtutzyPnZxpspcoboE/LPtDA7pr4C0aEdaD9bqhBWYLNBZLX+FVJaQRRnWwQkxHczWzGDDT2HkNoGz1TqmSX27lRHa5QDXZw0W6iR2LO8kDBliYU5tsM9Mb/UUDos5X1wZCP4FAj8OW5EEAYyBX8O6C9Fa0E3xEMypZ
;

[dil2.ebox-2.esplab.io](http://dil2.ebox-2.esplab.io/).  IN      TXT     "4gpWDNggpLRZHNuv6AcdfZJZBXSVJKoM7yN1gRtCdkCM3SW1uZYqvcqu7uE/PnD0CFhwhFPb/LlNelbed8E/Fhp4TUxZdltqlHYwbiCsosLXaY0A08InUhiW+15WPfk+mn29voKE2Ow6o" "+zKHrUaegeOodV3CKMy7UrfzbYlLjMzMAVrQbsaxfmh5He/4tBNSRN73Tzhtbr0A3kW+UPdzYbg3CBPnx3/fLmrqc4S6gKRhfYu6erC2ywmrwj/zshXXA63tISUO7yoslqCYhTm7++gzj" "W8nUybv2t2Ah4kBgnAkgCpxddAurnuGrloj3e/HbMqul2ONtUajTckP9DqqVpKzjK5JH7f0cCEXcBpJoWL7ZG1kHoD4PE2LQmFVZwQRPgBZ2B29InAJ+hADVQRr+Di+NmjzF15xwIVf2H" "IgFSPqJi6RmDkiZn9SvZvRJSUDwPqXn/t31ki2c3/mkn+KgX+ZKRkhRhZyzqFKCRcR+U3VvfsOAQVsJpEybJZ0jpMHnzIYZqo26YVfpf4/KOoSVFAkiPicx7lRgEFZAG3SRB1LLS3vqDa" "8W8mKsQSzD8f8g4WO2Pc4E/CtvGAGRswUyGVpa03qT6wvr4IA+Oy57gmMlJ+98zn8Eeg5nBCWCegXj2NGloClGNB0EN599EgQDJEauKMD/tQTfftZg/bUKn8+KJezHrAXzTWbEBfN0mV/RaObQF9tlEdW/gtMf6sGCBYbKSw3PT53fY2UmMDDxszuHDpMXmBoapeqrq/E1Nnu9/wTHTU5PEJgdYqrrdnl+gEDBg4WQ1JZXICUp6jV3ePt8AAAAAAAAAAAAAAA
;
```  

### B. TLSA records for ExpressPQDelivery   
```
_443._udp.ebox-dil.0.esplab.io.         IN      TLSA    3 0 0(
                  30820f8b308205ffa00302010202146e8f36bc074d6ee3fa3a660e5e3cce
                  6c37822956300d060b2b0601040102820b07040430123110300e06035504
                  030c0774657374204341301e170d3234303932333130333333335a170d32
                  35303932333130333333335a30123110300e06035504030c077465737420
                  434130820534300d060b2b0601040102820b07040403820521000c807fde
                  1fb5766dbfdf7fcabb630931952ad6f58e1d5bcf5988af2ce5ef08a3cada
                  8151ebe5e9e21562ceee978def7b54717d4fde6102f30318031154797eaa
                  7475eb018504eca10c5e915cf86d5dbdfde87cc6b7a8d7f1d2556868c8df
                  6398bc20914fa2f0b427b94e9e683752283826c026891a1a24e86a4553de
                  3d2c4b08659553a0b2ae2b4bda2caded405c1698108e05a15192e9f83ea6
                  cdaae495faf681a8ac738ac5e72f548d9d1156d7e96eb0cac1410c7fffa1
                  e6e1e6327be37c4977974bddd2f6902b4674b76c0be28a1acdb00f9a2b4e
                  e541c9fd305cce8bdf56158d56655f3e9cfe0644ec896e13b1e1f6dc309b
                  250d31f5a842a5321d6d84f0d9328bdb250b0c1d39188e341733781c1c6d
                  3814d6bab800ff2f962d37676e00933a5f7ef232d4c8ebd2cc1d09c03f4d
                  010e6cb42863848da8db5006e32926549091154e54559c23b60c6ff2da6b
                  941887f63de01c0c0620bb37334327779b83070449be98fdf3cb5b365217
                  71be74acc181fb1a78b931ac4c6a28d0437e549759ec28109508441181ff
                  c8e6c8793c875604cbd2d98a51f42ca513786918b27a859fe695fb2a791a
                  d2e5730f9c2e2e91c0898fa7fdd0fe93591105ee1c650a6c6193845fd954
                  ad46b3eff0cf85bee864cb7f76c71f3c5318c49923134581012da9998cae
                  6fcb012a8ea9dc502f7cee130b3c6c407b4978344a18848cd5c06b0e1fcd
                  a3301167c1d3593bd4221cd29bdb54dea234c96eecd741c5a70ff40289a9
                  ad1f62b5661dcbd309d06cba1d29af75ba74bdb43c5f964172fc8b73064c
                  d15e343eab11090ee09f20ae380a0c39554c9d73b553540471a6d6c01337
                  2e6f375e102b32dd107886d09ed8c22729d209fd6c2d848cc5e6d503fe3b
                  6cf1384779349eacba3b4e6b97bb9b7bf37068f6dd40975e9118af4f5391
                  425a900a44904db56443357601bf5aae0997ebfcebdbf9bda8941df002d1
                  6ef16479111c88822215ba1c5221dcd7ebdfec7a1b5e173b079e459cbeeb
                  8ee155dc9581a73fbe1e3c347b8ff3588f720b15d3a703d176591c1ce864
                  552dc9c6fef96ae83c9d3ce157cf513df215254937fa5b1c4a78fef7c1bf
                  5d687b22d7c5f4bc33c2183cf0fd57182e400550e2b3689c8e42c46fe535
                  446b1eb6ad0fbb279f0616d42b85952122b992e2c71a32a0dc166e60496e
                  4192e3173b34840f6560382591c2e62ce9aef669a8359052273736344e88
                  3d675025b3b78ee50f8622f1874bbb8e21bc4e814b9e0aa72b014761dc3c
                  7da2acb17ddacf608cbae86866670dcd68882cd1a41bbd1f52afbe2975ce
                  4a80529be1c87ba27b96
)

_443._udp.ebox-dil.1.esplab.io.         IN      TLSA    3 0 0(
                  06f1a0ec141c91bfe11e81ec3f662891188f287f13acf428d4aa8872f8a7
                  d478af662a9570bf554d72b5b24eda9f815f9032e6689cf4175181eebc05
                  e6879889d1cdbbf003f1701821ff4ef4317033090c729f82a339c8110813
                  e81ebd935616529ba9a65361a533aec445354dcac9a5f3987ec51a30cd2f
                  ecc06777083f6c77ed438a24a2e94344a056be0404e7c89ae6b1bccc22c6
                  16424c18d39fd94d6d42448be7e236a518fa96554cc0ad4ec9bb2022141b
                  deb41f7c97eb5472b9adf31820a2e3ce0af77c05a8e3413462465ad659bd
                  2456b00a2e2a0b113f2fd6d35ac777ea11e9b1811eac5aaf079dc9c93583
                  d134691d54e71badb6a2b824d98f1b5eb75e4bd7df0cc98ed64d35467ee4
                  a8d289f5da83bf696a9ac714c3dd4c3b6aa4e45727bb0d39204145f9cbad
                  74ac610ceaff3975a781fa301b472385bc32ea78e9b0792dc26ffda344b1
                  edfb08d478bf2314b615abb0f4cd8f98227a0405a2424343655d21481528
                  9373111dc4cc640fa3533051301d0603551d0e041604140e33144573791f
                  16f60d8ccca03ad409a1ca009f301f0603551d230418301680140e331445
                  73791f16f60d8ccca03ad409a1ca009f300f0603551d130101ff04053003
                  0101ff300d060b2b0601040102820b070404038209750009a6627b676c8c
                  6454d7ae1ee576e1e17877dea5af31fa49369e8902f47fe6bac920ca3f72
                  0ae83ef7bd8014f13da9519c13ac41c0ff83b1a414d0176446102bab58cc
                  ecaef9d7ab7c0c0191c23b04fd8b6be22230db3bda9dcc6bd3efadcbd968
                  3c2ae57664a45bf1318adf79b69e74bc8c79c5cf1cdd06a7fe8b90afe680
                  de4167e0dce9d646f8a3b6b4d368788527211851ea15bf7b8d68230fa43f
                  54d5eadf207ab2dbb2b2f6e6270e8be896f1b75f1cd36566285309bab111
                  98d19a062553ad5087358b999242f3108979b4790c8e7fd0ee030ea6d2f6
                  596cf630906d50034109f8c5118d7b588ba0592fda897ed3b88238293147
                  10c1aa735493cbe694e3fec80cc219d37e1c5f2618e16f9897d9614a4c33
                  49ad8781fd0f44d619b2ea62affc2242e63cff54f53939d441975ee3ae21
                  b28426755297ae277934ba404d1c83f26f6218098cfea3acb860a42375af
                  d73cd54016d5d334f41eb85d1acdc4f949aae6e6cc9927555caf0e88efcb
                  ce29463bfd493132dd1b83acfc35ed44671c194e30af33a9b61479dd6c1f
                  25b89b56457539c11c91349ed6c7e791eb15f8b3b785cf2b7b01b1226c75
                  2cd551aeb0bb47a25d7028721f11b37f045ddd51238b279e41019185d220
                  1896cf656e2fca958319cfe5b4fad0a0e23520617c165050fbf8cc25c865
                  af9f8028cca3cfe6df21ca0ac35b0faace138152617a2e93b61d10f077da
                  982137e7ba64e050210f8c32531a45d4b039b60bb69266a5785a19247d77
                  400953ab60348959b09c115cecb417a441945b7b42c9a07f4b6f91cc90c4
                  df7ceff46107c05b0a4f97119debf905e3e0ef15bbe73f1f7956552609ee
                  7d1ab87c7238ae6a607b
)

_443._udp.ebox-dil.2.esplab.io.         IN      TLSA    3 0 0(
                  015d2d26aec277b020eac4d172e963128e9ef3f17ae85ed008d92a029efb
                  29800f88b4df3c5dd8b178323cfa73174e4e294f3f72b9ec8a1cbb97d510
                  d02e1c8f7f4e8bdb1768412305d9103217dc75ead4df3bf4a3b40a4e502e
                  2d5b2f66fcd4832c2b6a8585d63593dea1ef69173f8d910e004dc527a710
                  0706cdd2333c7b127da84b069376b0657e21617ea5f8e9a7cd0a28997e44
                  8f7ef2eb34f56a6503ce19ae089a9ad8cbb1bd4ce014efa44822d75599e9
                  d1f8041b0f4ee1583ddc146f6babb7a27fb7727dcf49660a8066057e5e68
                  6476a5a97f841243df97812e57762677a26462c3d24d0067635f432aec62
                  9eccc57ab27b80453927f9e422bdf6842157bbef63c1ef516347f54a54cf
                  6aa39818d4a23e30047a925351992b7735369cc16826597f9f683c9eb6c9
                  bd067d7c6b5591e3d868cb3659bd00c6f4309a70f3fc2db3ae206f942322
                  87a53ab87782e71bd528edd0935ecd29abfd7113b1208d1a2ad7d3233836
                  c7fe988dc8c84657b565229e7fc42605078bc86c3fcc5b4ea9e0894f0f12
                  74df87ba83ca6635bbdb15e86a5616d5c4115ec02315947782b271358075
                  5e976cbf12ba82646ad49469d9de7c2eb72e73badad7ac322d84f9f699b6
                  34fced1505b52d36c7559d8b7afca1c3a98670f0b92e8273f044468aa369
                  b5e646ac34aa6c61053522048a604298e1c62ee14b46344e9806f698a5f0
                  63fea5e3add0c373650ce9b9110e73989f7eebdefda9f3978e87e00a471b
                  31211a5203f93e89178f9e7d92382a561d515670a348019cb29bdf09d081
                  8e1f93c2038a832121653f12721cd9f650b6c00b7d37163d8f05e99bb715
                  e235b040cb6997043ab3495b8e7e42f6694a2ab155c49d11e807e41fd268
                  a767dd6b306f17b92896c837cfa6403ef8742203a5656c1551b64a1ba720
                  afdf4709afd74df6a2934ba29a973d184305834fb03fea737df5b303a6a2
                  5ed6e32b84909afb7b051814ab9336395fb379bdb0f34cc6903c1e42440d
                  06bb9f6c78a6908041582df991e5e946bee8d38a4d4859fa16d5df6016c3
                  98e15913041b2d925c18cc2133b4fecaa2d9daaf8cf74e751b8d7676e57c
                  c087fc5f46e0af652ff2156f97e2d79219b6a0d67a19c76ef8ab008ba48a
                  552ce50cbde9515c26fe3de69b0d55dfa1ef445ee76c8fb5b7da1e066a4b
                  b44bf04b487479586ee39118a7325c62bf0b98198135a639613efb50306c
                  0f1c102e4d3c207f6e0af18bcea8816cd3633c29eca45f27182db21ff74f
                  aa27409c80713207a0086369ddb9f6ec971ed6fe15a76ef8cc9e09e59d82
                  eda29793a2ee0f01eeba5212518b4dfe84aedba6b6e731d2b9ec56ab801c
                  e412bb48a5723414402792503c98c14b4b59b4dad4d4fe83feb33c6be8c5
                  80c2755443379f6ace1d5ec08d8f37f64845229dd44dbd4b54571ad3c246
                  eb269d9ed4e6fcf4c7285d3b27398505f7c2cc921960a426aa7e3c63b845
                  1b832c171881a73a2b01fae7a1952537797d23bab50adcb40a3f432b0544
                  7f4935302ae5c7f8b0c7
)

_443._udp.ebox-dil.3.esplab.io.         IN      TLSA    3 0 0(
                  7c15469d52123da57940f45cea5af247dcd6f6ebb7f1a52e854c5c3d90d8
                  dadfc43d4fd3c1179fee526d4f85fbe9d70ac4ca47612071834313e7b34c
                  12cbd7292691aa9849b5af3e43f03468f3459d92090f0fa86e3a9a8da840
                  4d6cf8a581bffce808d26816af1853a462ba2a3b54b101ba8ecd2f46faa9
                  d3de605c9b713404e76ac3a4bf12d5b2d0ed6b23dda71c890fa55c1c6aca
                  8d4e207d3fdc340d23f65a544f1cb916d2a0efa35a28a6d07754acdc2b0e
                  cf01348b19f17f7d4cda9f358d4b70528e337945ef69e73fe67a38ce5d49
                  1b167557f2634cb291b9d3ec97b4318ef1d588115db87837b86923215a36
                  f9737d83ff36d9fc1690cacee4e1818c4f717814799d5c79a188ddcbbbb5
                  ec3ed640f76353013f9567bdf635747566a6414443fcb8a168ea607f1f35
                  dc8500e9edc52cf70e6173670008077aee0b854058c587a4be5f100db58a
                  f2eb41dcfe6f1c2aed00cfcc2ac3b2f067e9bd344744f27d48cbc48cb0ec
                  0b6722255d3d751765936d473cfe616699d3504805a10161cdeda89b386e
                  fcf612bb5e1336522b371b72ae9ec1e93c711bbc75e4870865c4e3766f3c
                  1f797dcdb3d5560568861ae8c8d12cfe8e53422b1917570e41c0e8db39d9
                  e61520a2fd0a73aec70fa1c52a7ee371c995eca4720d3d1c841edef8dc6a
                  c901b63bbfebfa6eb204448091986f2a9e70be96dead3c2cca445883a765
                  3eb272ac3c7673eac1b6bd204b8cc2fa2ed594376d2acc58dc5daa969752
                  e25c5845cfb80747ada9d7fadd041991b95d6196ae9192541d59896dc398
                  fec1c74995dcff7a60a3618d8b57283a1a21c0563b4d7d37a9ae295ab38d
                  8ab781f13ea6e86da0dc219e4b2808b9ca8b89440dd6f11c6618e241d00c
                  12364f6885a6c8def214172a2d2f3360778298a7b6c3d9dce7092d555864
                  7c868a92aeafb1c4ce2d303d586172838c8d9dc1c7d4dbedee0000000000
                  000000000000000000000000000000000000000a1a2838
)
```  
__Please Check _exampe_zonefile.txt_ for more detail informations for generate DNS records__

## Reference
<https://github.com/open-quantum-safe/oqs-provider/blob/main/USAGE.md?plain=1>
