from django.contrib import admin
from apps.models import Cliente, Tenico, Servicio, Movil, Diagnostico, Repuestos, FacturaDetalle, Factura
# Register your models here.


class Clienteadmin(admin.ModelAdmin):

    list_display =['Nombre_Completo', 'telefono']
    list_filter = ['tipo', 'gender']
    search_fields = ['nit','nombres','apellidos']

class TecnicoAdmin(admin.ModelAdmin):

    list_display =['Nombre_Completo', 'telefono']
    list_filter = ['gender']
    search_fields = ['nit','nombres','apellidos']

class MovilAdmin(admin.ModelAdmin):

    list_display =['Marca', 'modelo', 'only_year']
    list_filter = ['ano']
    search_fields = ['Marca','modelo','ano','imei']

class DiagnosticoAdmin(admin.ModelAdmin):

    list_display =['fechadiag', 'tecnico_diag', 'descripcion', 'propietario','marca','modelo']

    def propietario(self, obj):
        return obj.serv.movil.propietario.nombres

    def marca(self, obj):
        return obj.serv.movil.Marca
    def modelo(self, obj):
        return obj.serv.movil.modelo

class FacturaDetalleAdmin(admin.TabularInline):
    model = FacturaDetalle
    exclude = ['subtotal']


class FacturaAdmin(admin.ModelAdmin):
    raw_id_fields = ['diag']
    inlines = [
        FacturaDetalleAdmin,
    ]

    list_display = ['date', 'get_tenico','get_customer','get_customernit','total']
    search_fields = ['diag__tecnico_diag__nombres','diag__serv__movil__propietario__nit', 'diag__serv__movil__'                                                                                       'propietario__nombres']
    list_filter = ['date','diag__tecnico_diag__nombres']

    def get_customernit(self, obj):
        return obj.diag.serv.movil.propietario.nit

    def get_customer(self, obj):
        return obj.diag.serv.movil.propietario.nombres

    def get_tenico(self, obj):
        return obj.diag.tecnico_diag.nombres




admin.site.register(Cliente, Clienteadmin)
admin.site.register(Tenico,TecnicoAdmin)
admin.site.register(Servicio)
admin.site.register(Movil, MovilAdmin)
admin.site.register(Diagnostico, DiagnosticoAdmin)
admin.site.register(Repuestos)
admin.site.register(Factura,FacturaAdmin)


