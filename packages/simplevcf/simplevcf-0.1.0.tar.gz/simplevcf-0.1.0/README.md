# simplevcf

![Python package](https://github.com/informationsea/simplevcf-py/workflows/Python%20package/badge.svg)

Simple VCF parser/writer with pure python

## Examples

### Read VCF

```python
    with simplevcf.vcfopen('some.vcf.gz') as reader:
        for record in reader:
            # process a record
```


### Read, manipulate and write

```python
    with simplevcf.vcfopen('some.vcf.gz') as reader, with open('output.vcf) as f:
        writer = simplevcf.Writer(f, reader.headers,
                                  reader.samples)
        for record in reader:
            # manipulate a record
            writer.write_record(one)
```

### Access to INFO and CALL

```python
    with simplevcf.vcfopen(test_file) as reader:
        for one in reader:
            print(
                one.INFO['AC'], one.CALL['ERP107576_NovaSeq_SAMEA104707359']['GT'][0])
```