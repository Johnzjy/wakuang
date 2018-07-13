import unittest
import sys
sys.path.append("..")
from src.tdx import TDX 

uut =TDX()

class TdxUnitTest(unittest.TestCase): #继承测试
    """
    Tdx Unit Test is test class TDX
    """
    def setUp(self):
        print("\n__________test begin_________")
        pass
    def tearDown(self):
        print ("__________test done !________\n\n")
        pass
    def test_init(self):
        print("test init")

    def test_IP(self):
        print("TDX IP : %s"%uut.IP)
        self.assertEqual(uut.IP,"119.147.212.81",msg="IP is wrong number.")
    def test_port(self):
        print("TDX port : %s"%uut.PORT)
        self.assertEqual(uut.PORT,7709,msg="port is wrong number.")
    def test_code(self):
        print("TDX init code : %s"%uut.code)
        self.assertIsNotNone(uut.code,msg="this init code has errro")
        uut.code="600339"
        print("TDX init code : %s"%uut.code)
        self.assertEqual(uut.code,"600339",msg="code setter is wrong number.")
    def test_get_data(self):
        print ("\n\n\"\"\"test TDX get_day_data_tdx. \n"\
               "this funcion will return DateFrom.\"\"\"")
        uut.code="600339"
        data=uut.get_day_data_tdx()
        print("\n\ntype is ",type(data))
        self.assertEqual("%s"%type(data),"<class 'pandas.core.frame.DataFrame'>",msg="wrong!")
        print ("\n\n  the exmple for hard one")
        print("~"*30)
        print(data.iloc[1])
        print("~"*30)
    def test_get_sh_list(self):
        """
        get down the shang hai list ;then test it not None
        """
        print ("\n\nget shang hai list ")
        data= uut.get_sh_list()
        self.assertIsNotNone(data)


    
            
def suite():
    """
    构建自己的测试集
    """
    suite = unittest.TestSuite()
    suite.addTest(TdxUnitTest('test_IP'))
    suite.addTest(TdxUnitTest('test_port'))
    suite.addTest(TdxUnitTest('test_code'))
    suite.addTest(TdxUnitTest('test_get_data'))
    #suite.addTest(TdxUnitTest('test_get_sh_list'))
    return suite

if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())