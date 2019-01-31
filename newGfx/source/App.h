/**
  \file App.h

  The G3D 10.00 default starter app is configured for OpenGL 4.1 and
  relatively recent GPUs.
 */
#pragma once
#include <G3D/G3D.h>

/** \brief Application framework. */
class App : public GApp {
protected:
    const int                       numReticles = 55;

    shared_ptr<GFont>               m_outputFont;
    shared_ptr<Texture>             m_reticleTexture;

    /** Used to detect GUI changes to m_reticleIndex */
    int                             m_lastReticleLoaded = -1;
    int                             m_reticleIndex = 0;
    float                           m_sceneBrightness = 1.0f;

    /** Called from onInit */
    void makeGUI();

public:
    
    App(const GApp::Settings& settings = GApp::Settings());

    /** Call to change the reticle. */
    void setReticle(int r);

    /** Increment the current reticle index */
    void nextReticle() {
        setReticle((m_reticleIndex + 1) % numReticles); 
    }

    /** Call to set the 3D scene brightness. Default is 1.0. */
    void setSceneBrightness(float b);

    virtual void onInit() override;
    virtual void onAI() override;
    virtual void onNetwork() override;
    virtual void onSimulation(RealTime rdt, SimTime sdt, SimTime idt) override;
    virtual void onPose(Array<shared_ptr<Surface> >& posed3D, Array<shared_ptr<Surface2D> >& posed2D) override;
    virtual void onAfterLoadScene(const Any& any, const String& sceneName) override;
    virtual void onGraphics2D(RenderDevice* rd, Array<shared_ptr<Surface2D> >& surface2D) override;
    virtual bool onEvent(const GEvent& e) override;
    virtual void onUserInput(UserInput* ui) override;
    virtual void onCleanup() override;
};