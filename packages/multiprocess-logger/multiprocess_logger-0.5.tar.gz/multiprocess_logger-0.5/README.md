###                                                                        多进程日志切换处理器

- 一个安全可靠高效的进程间日志处理器  A safe, reliable and efficient inter process log processor fix bugs 修复上一版的bug

- speed about 7100 lines/s 0.8M/s (10 processes) 7100行/s 0.8M/s 测试环境 虚拟机(virtual machine) 

- CentOS7 64 

- python3.7 

- 机械硬盘 hard disk

- 添加测试用例

- 新增参数 need_zip 是否需要日志压缩 布尔值 (需要以命名关键字参数传入)

- 新增参数 compresslevel 日志压缩的gzip等级 默认为9 (需要以命名关键字参数传入)

- v 0.5 修复上一版(0.4)的bug

- ```
  import logging
  
  from multiprocessing import Process
  from logging import Formatter
  
  from multiprocess_logger import MultiprocessingHandler
  
  handler = MultiprocessingHandler(filename='./ppp.log',
                                   maxBytes=1024 * 1024, backupCount=10, need_zip=True, compresslevel=9)
  fmt = Formatter(fmt='%(asctime)s - %(process)d - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
  handler.setFormatter(fmt=fmt)
  logger = logging.getLogger('SHIT')
  logger.addHandler(handler)
  logger.setLevel(logging.INFO)
  
  logging.basicConfig(level=logging.ERROR,
                      format='%(asctime)s - %(process)d - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
  
  
  def write_log():
      while True:
          logger.info('Hello World!------------Hello World!')
  
  
  if __name__ == '__main__':
      # write_log()
      p_list = []
      for i in range(6):
          p_list.append(Process(target=write_log))
  
      for i in p_list:
          i.start()
  
  
  ```

  




