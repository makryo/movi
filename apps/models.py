from django.db import models
from django.db.models import Sum

SELECCION_GENERO = (

    ('M', 'Masculino'),
    ('F', 'Femenino'),
)

TIPO_CLIENTE = (

    ('E', 'Empresa'),
    ('I', 'Individual'),
)
TIPO_SERVICIO = (

    ('R', 'Reparación'),
    ('C', 'Remplazo'),
    ('M', 'Mantenimiento'),
    ('S', 'Software'),
)
# Create your models here.
class Persona(models.Model):
    nombres = models.CharField('Nombre:', max_length=50, help_text='Ingrese su nombre Completo')
    apellidos = models.CharField('Apellidos:', max_length=50, help_text='Ingrese sus Apellidos')
    nit = models.CharField('Nit:', max_length=100, help_text='Ingrese Nit')
    fechanacimiento = models.DateField('Fecha de Nacimiento', help_text='Ingrese Fecha de Nacimiento', blank=True, null=True)
    cui = models.BigIntegerField('DPI/CUI:', help_text='Ingrese Numero De Identificación Personal', blank=True,
                                 null=True)
    gender = models.CharField('Genero:', max_length=1, choices=SELECCION_GENERO, default='M',
                              help_text='Selección de Género')
    direccion = models.CharField('Dirección:', max_length=100, help_text='Ingrese Dirección')
    email = models.CharField('Email:', max_length=50, help_text='Ingrese el correo electronico que utiliza', blank=True,
                             null=True)
    telefono = models.BigIntegerField('Telefono de Casa:', help_text='Ingrese un número de telefono de casa')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Creado')
    modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='Modificado')

    def __str__(self):
        return '%s %s' % (self.nombres, self.telefono)

    class Meta:
        abstract = True


#####################################################################################################


class Cliente(Persona):

    tipo = models.CharField('Tipo de Cliente:', max_length=1, choices=TIPO_CLIENTE, default='I',
                              help_text='Selección de tipo de cliente')

    def __str__(self):
        return '%s %s' % (self.nombres, self.apellidos)

    def Nombre_Completo(self):
        return self.nombres + ' ' + self.apellidos
        Nombre_Completo.short_description = "Nombre Completo"

        n_completo = property(Nombre_Completo)

    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'


#########################################################################################################
class Tenico(Persona):

    fechacontra= models.DateField('Fecha de Contratación',
                                       help_text='Ingrese Fecha de Contratación', blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.nombres, self.apellidos)

    def Nombre_Completo(self):
        return self.nombres + ' ' + self.apellidos
        Nombre_Completo.short_description = "Nombre Completo"

        n_completo = property(Nombre_Completo)

    class Meta:
        verbose_name='Técnico'
        verbose_name_plural='Técnicos'

###########################################################################################
class Movil(models.Model):
    propietario = models.ForeignKey(Cliente, null=False, on_delete=models.CASCADE)
    Marca= models.CharField('Marca:', max_length=50, help_text='Ingrese la Marca')
    modelo=models.CharField('Modelo:', max_length=50, help_text='Ingrese el modelo')
    imei=models.CharField('Imei:', max_length=50, help_text='Ingrese el IMEI (BAJO LA BATERIA O EN CONFIGURACIÓN')
    ano=models.DateField()
    color=models.CharField('Color:', max_length=50, help_text='Ingrese el color')
    observaciones=models.TextField('Observaciones:', max_length=500, help_text='Ingrese la observacion')



    def __str__(self):
        return '%s %s' % (self.Marca, self.modelo)


    @property
    def only_year(self):
        return self.ano.strftime('%Y')

    class Meta:
        verbose_name='Móvil'
        verbose_name_plural='Móviles'

###################################################################################################

class Servicio(models.Model):
    nombre = models.CharField('Tipo de Servicio:', max_length=1, choices=TIPO_SERVICIO, default='R',
                              help_text='Selección de Servicio')
    movil = models.ForeignKey(Movil, null=False, on_delete=models.CASCADE)


    def __str__(self):
        return '%s %s %s' % (self.nombre, self.movil.Marca, self.movil.propietario.Nombre_Completo())


    class Meta:
        verbose_name='Servicio'
        verbose_name_plural='Servicios'
#####################################################################################################

class Diagnostico(models.Model):
    fechadiag= models.DateField('Fecha de Contratación',
                                   help_text='Ingrese Fecha de Contratación', blank=True, null=True)
    tecnico_diag = models.ForeignKey(Tenico,null=False, on_delete=models.CASCADE)
    serv = models.ForeignKey(Servicio, null=False, on_delete=models.CASCADE)

    descripcion=models.TextField('Descripción:', max_length=500, help_text='Ingrese la Descripción')

    def __str__(self):
        return '%s %s' % (self.fechadiag, self.descripcion)

    class Meta:
        verbose_name='Diagnóstico'
        verbose_name_plural='Diagnósticos'


################################################################################################################

class Repuestos(models.Model):
    nombre=models.CharField('Nombre:', max_length=50, help_text='Ingrese el nombre')
    Marca= models.CharField('Marca:', max_length=50, help_text='Ingrese la Marca')
    Price = models.DecimalField('Précio', max_digits=18, decimal_places=2)
    cantidad = models.FloatField('Existéncia')
    observaciones=models.TextField('Observaciones:', max_length=500, help_text='Ingrese la observacion')



    def __str__(self):
        return '%s %s' % (self.nombre, self.Marca)

    class Meta:
        verbose_name='Repuesto'
        verbose_name_plural='Repuestos'


#############################################################################################################

class Factura(models.Model):

    diag = models.ForeignKey(Diagnostico, on_delete=models.CASCADE)
    date = models.DateField('Fecha')
    total = models.FloatField('Total', null=True, blank=True)

    class Meta:
        verbose_name = 'Facturación'
        verbose_name_plural = 'Facturaciones'

    def save(self, *args, **kwargs):
        total = self.details.all().aggregate(Sum('subtotal'))
        self.total = total['subtotal__sum']
        super(Factura, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.diag,  self.total)
##########################################################################################


class FacturaDetalle (models.Model):

    fac = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Repuestos, on_delete=models.CASCADE)
    quantity = models.IntegerField('Cantidad')
    subtotal = models.FloatField()

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Facturas'

    def save(self, *args, **kwargs):
        product = Repuestos.objects.get(id=self.product.id)
        product.cantidad = product.cantidad - self.quantity
        product.save()
        self.subtotal = self.product.Price * self.quantity
        super(FacturaDetalle, self).save(*args, **kwargs)