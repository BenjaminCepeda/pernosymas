# Validación de Cédula y RUC para Ecuatorianos en Python compatible con 2.7 y 3.4 en adelante.
# Ligeramente modificado para validar las cedulas 23 (Sto Dgo, :D soy de ahí) y 24 (Santa Elena).
# Tomado de aquí: https://fecyman10.wordpress.com/2014/05/01/validar-cedula-y-ruc-ecuatorianos-en-python/

class PymUtil(object):
    @staticmethod
    def verificar(nro):
        l = len(nro)
        if l == 10 or l == 13:  # verificar la longitud correcta
            cp = int(nro[0:2])
            if cp >= 1 and cp <= 24:  # verificar codigo de provincia
                tercer_dig = int(nro[2])
                if tercer_dig >= 0 and tercer_dig < 6:  # numeros enter 0 y 6
                    if l == 10:
                        return PymUtil.validar_ced_ruc(nro, 0)
                    elif l == 13:
                        return PymUtil.validar_ced_ruc(nro, 0) and nro[
                                                             10:13] == '001'  # se verifica que los ultimos numeros sean 001
                elif tercer_dig == 6:
                    return PymUtil.validar_ced_ruc(nro, 1) and nro[
                                                         10:13] == '001'  # sociedades publicas
                elif tercer_dig == 9:  # si es ruc
                    return PymUtil.validar_ced_ruc(nro, 2) and nro[
                                                         10:13] == '001'  # sociedades privadas
                else:
                    raise Exception('Tercer digito invalido')
            else:
                raise Exception('Codigo de provincia incorrecto')
        else:
            raise Exception('Longitud incorrecta del numero ingresado')

    @staticmethod
    def validar_ced_ruc(nro, tipo):
        total = 0
        if tipo == 0:  # cedula y r.u.c persona natural
            base = 10
            d_ver = int(nro[9])  # digito verificador
            multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
        elif tipo == 1:  # r.u.c. publicos
            base = 11
            d_ver = int(nro[8])
            multip = (3, 2, 7, 6, 5, 4, 3, 2)
        elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
            base = 11
            d_ver = int(nro[9])
            multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
        for i in range(0, len(multip)):
            p = int(nro[i]) * multip[i]
            if tipo == 0:
                total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
            else:
                total += p
        mod = total % base
        val = base - mod if mod != 0 else 0
        return val == d_ver
