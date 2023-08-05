#ifndef GLOG_SINGLETON_HPP
#define GLOG_SINGLETON_HPP

#include <glog/logging.h>

class GlogSingleton
{
public:
     static GlogSingleton &instance();

private:
     GlogSingleton();

     ~GlogSingleton();
};

#endif
