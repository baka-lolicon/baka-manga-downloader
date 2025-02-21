var LZString = (function() {
    var f = String.fromCharCode;
    var keyStrBase64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var baseReverseDic = {};
    function getBaseValue(alphabet, character) {
        if (!baseReverseDic[alphabet]) {
            baseReverseDic[alphabet] = {};
            for (var i = 0; i < alphabet.length; i++) {
                baseReverseDic[alphabet][alphabet.charAt(i)] = i
            }
        }
        return baseReverseDic[alphabet][character]
    }
    var LZString = {
        decompressFromBase64: function(input) {
            if (input == null)
                return "";
            if (input == "")
                return null;
            return LZString._0(input.length, 32, function(index) {
                return getBaseValue(keyStrBase64, input.charAt(index))
            })
        },
        _0: function(length, resetValue, getNextValue) {
            var dictionary = [], next, enlargeIn = 4, dictSize = 4, numBits = 3, entry = "", result = [], i, w, bits, resb, maxpower, power, c, data = {
                val: getNextValue(0),
                position: resetValue,
                index: 1
            };
            for (i = 0; i < 3; i += 1) {
                dictionary[i] = i
            }
            bits = 0;
            maxpower = Math.pow(2, 2);
            power = 1;
            while (power != maxpower) {
                resb = data.val & data.position;
                data.position >>= 1;
                if (data.position == 0) {
                    data.position = resetValue;
                    data.val = getNextValue(data.index++)
                }
                bits |= (resb > 0 ? 1 : 0) * power;
                power <<= 1
            }
            switch (next = bits) {
            case 0:
                bits = 0;
                maxpower = Math.pow(2, 8);
                power = 1;
                while (power != maxpower) {
                    resb = data.val & data.position;
                    data.position >>= 1;
                    if (data.position == 0) {
                        data.position = resetValue;
                        data.val = getNextValue(data.index++)
                    }
                    bits |= (resb > 0 ? 1 : 0) * power;
                    power <<= 1
                }
                c = f(bits);
                break;
            case 1:
                bits = 0;
                maxpower = Math.pow(2, 16);
                power = 1;
                while (power != maxpower) {
                    resb = data.val & data.position;
                    data.position >>= 1;
                    if (data.position == 0) {
                        data.position = resetValue;
                        data.val = getNextValue(data.index++)
                    }
                    bits |= (resb > 0 ? 1 : 0) * power;
                    power <<= 1
                }
                c = f(bits);
                break;
            case 2:
                return ""
            }
            dictionary[3] = c;
            w = c;
            result.push(c);
            while (true) {
                if (data.index > length) {
                    return ""
                }
                bits = 0;
                maxpower = Math.pow(2, numBits);
                power = 1;
                while (power != maxpower) {
                    resb = data.val & data.position;
                    data.position >>= 1;
                    if (data.position == 0) {
                        data.position = resetValue;
                        data.val = getNextValue(data.index++)
                    }
                    bits |= (resb > 0 ? 1 : 0) * power;
                    power <<= 1
                }
                switch (c = bits) {
                case 0:
                    bits = 0;
                    maxpower = Math.pow(2, 8);
                    power = 1;
                    while (power != maxpower) {
                        resb = data.val & data.position;
                        data.position >>= 1;
                        if (data.position == 0) {
                            data.position = resetValue;
                            data.val = getNextValue(data.index++)
                        }
                        bits |= (resb > 0 ? 1 : 0) * power;
                        power <<= 1
                    }
                    dictionary[dictSize++] = f(bits);
                    c = dictSize - 1;
                    enlargeIn--;
                    break;
                case 1:
                    bits = 0;
                    maxpower = Math.pow(2, 16);
                    power = 1;
                    while (power != maxpower) {
                        resb = data.val & data.position;
                        data.position >>= 1;
                        if (data.position == 0) {
                            data.position = resetValue;
                            data.val = getNextValue(data.index++)
                        }
                        bits |= (resb > 0 ? 1 : 0) * power;
                        power <<= 1
                    }
                    dictionary[dictSize++] = f(bits);
                    c = dictSize - 1;
                    enlargeIn--;
                    break;
                case 2:
                    return result.join('')
                }
                if (enlargeIn == 0) {
                    enlargeIn = Math.pow(2, numBits);
                    numBits++
                }
                if (dictionary[c]) {
                    entry = dictionary[c]
                } else {
                    if (c === dictSize) {
                        entry = w + w.charAt(0)
                    } else {
                        return null
                    }
                }
                result.push(entry);
                dictionary[dictSize++] = w + entry.charAt(0);
                enlargeIn--;
                w = entry;
                if (enlargeIn == 0) {
                    enlargeIn = Math.pow(2, numBits);
                    numBits++
                }
            }
        }
    };
    return LZString
}
)();
String.prototype.splic = function(f) {
    return LZString.decompressFromBase64(this).split(f)
}

function decode_splic(input){
	return input.splic('|');
}

function decode_manga(p, a, c, k, e, d) {
	e = function(c) {
		return (c < a ? "" : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
	}
	;
	if (!''.replace(/^/, String)) {
		while (c--)
			d[e(c)] = k[c] || e(c);
		k = [function(e) {
			return d[e]
		}
		];
		e = function() {
			return '\\w+'
		}
		;
		c = 1;
	}
	;while (c--)
		if (k[c])
			p = p.replace(new RegExp('\\b' + e(c) + '\\b','g'), k[c]);
	return p;
}
console.log(decode_manga('V.M({"x":4,"w":"v","u":"4.2","t":s,"r":"q","p":["o.2.3","n.2.3","l.2.3","k.2.3","j.2.3","i.2.3","h.2.3","g.2.3","f.2.3","d.2.3","c.2.3","b.2.3","a.2.3","9.2.3","8.2.3","7.2.3","6.2.3","z.2.3","A.2.3","B.2.3","C.2.3","Q.2.3","R.2.3","S.2.3","P.2.3","U.2.3","10.2.3"],"W":X,"Y":Z,"T":"/N/y/O/L/","K":1,"J":"","I":H,"G":0,"F":{"e":E,"m":"D"}}).5();', 62, 63, 'D7BWAcHNgdwUwEbmAdgKwA4AMxwCc4BJAOwEsAXYLARgDYaUrq0bamAWGtJgZhvaYAmGjybUagplhrUqWAJw0cc7ArkppGOfSyNpLLG2mcs3aXywDpwrKLnisk6c9kAzUgBs4AZ2CBb90Bx72AAY2IAQwBbOGBaDBQeWWDSABNgJFJg4EAAOUBno0BQ2MAuuTTwqLSUkAYaLSqaeSZFYSobQVkADzwAaw6AOQBPAAtk1oBHSAB5AGFQYgmALwBlD1msAEVganj0dgx5eVlvD1wCADdCVNj5dgFiOFbyM7SPAHtgjoB9YMzvcjDyAFdfNJgKQIpAACK/MK4byiXqkYZ/MLEYL9MJPAjEJqcQRmFqOJyCYSCUSOPiCATgX79JosQRseYAWQAEsB3GRvP04KlXGEPN5ol5MYI9HTHCggA=='['\x73\x70\x6c\x69\x63']('\x7c'), 0, {}))