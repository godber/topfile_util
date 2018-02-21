base:
    '*':
      - common-packages

    'E@r1[012]c1n1.example.lan':
      - elasticsearch.master
      - logstash

    'E@r1[0123456789]c2n\d*.example.lan':
      - elasticsearch.data
      - logstash
    
    r10c1n2.example.lan:
      - logstash