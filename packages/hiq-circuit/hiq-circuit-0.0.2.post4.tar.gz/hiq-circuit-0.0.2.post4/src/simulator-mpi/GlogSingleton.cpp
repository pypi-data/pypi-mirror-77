#include "GlogSingleton.hpp"

GlogSingleton &GlogSingleton::instance()
{
  static GlogSingleton qqq;
  return qqq;
}

GlogSingleton::GlogSingleton()
{
  google::InitGoogleLogging("SimulatorMPI");
}

GlogSingleton::~GlogSingleton()
{
  google::ShutdownGoogleLogging();
}
