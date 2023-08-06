import tributary.streaming as ts
import pytest


class TestKafka:
    @pytest.mark.skipif("int(os.environ.get('TRIBUTARY_SKIP_DOCKER_TESTS'))")
    def test_kafka(self):
        '''Test streaming with Kafka'''
        def foo():
            yield 'a'
            yield 'b'
            yield 'c'

        out = ts.KafkaSink(ts.Foo(foo), servers='localhost:9092', topic='tributary')
        assert ts.run(out) == ['a', 'b', 'c']
