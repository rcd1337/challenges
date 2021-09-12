from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"(id: {self.id}) (name: {self.name}) (created_on: {self.created_on})"


class Currency(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    symbol = models.CharField(max_length=255, blank=False, null=False)
    indexed_value = models.DecimalField(max_digits=14, decimal_places=2, blank=False, null=False)
    
    def __str__(self):
        return f"(id: {self.id}) (code: {self.code}) (name: {self.name}) (symbol: {self.symbol}) (indexed_value: {self.indexed_value})"


class Operation(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="operations")
    source_currency = models.ForeignKey("Currency", on_delete=models.CASCADE, related_name="source_operations")
    target_currency = models.ForeignKey("Currency", on_delete=models.CASCADE, related_name="target_operations")
    source_amount = models.DecimalField(max_digits=21, decimal_places=8, blank=False)
    converted_amount = models.DecimalField(max_digits=21, decimal_places=8, blank=False)
    fee_amount = models.DecimalField(max_digits=20, decimal_places=8, blank=False)
    total = models.DecimalField(max_digits=21, decimal_places=8, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"""(id: {self.id}) (source: {self.source_currency}) (target: {self.target_currency})
        (amount: {self.source_currency}) (converted: {self.converted_amount}) (fee: {self.fee_amount})
        (total: {self.total})(created_on: {self.created_on})"""