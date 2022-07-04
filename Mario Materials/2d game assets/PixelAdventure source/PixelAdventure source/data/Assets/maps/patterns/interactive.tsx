<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.4" tiledversion="1.4.3" name="interactive" tilewidth="128" tileheight="64" tilecount="26" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="1" type="AnimatedTile">
  <properties>
   <property name="animated_type" value="Floating"/>
  </properties>
  <image width="32" height="10" source="../../Free/Traps/Falling Platforms/Off.png"/>
 </tile>
 <tile id="2">
  <image width="24" height="8" source="../../Free/Traps/Fan/Off.png"/>
 </tile>
 <tile id="3">
  <image width="16" height="32" source="../../Free/Traps/Fire/On (16x32)/0.png"/>
 </tile>
 <tile id="4">
  <image width="32" height="8" source="../../Free/Traps/Platforms/Brown Off.png"/>
 </tile>
 <tile id="5">
  <image width="32" height="8" source="../../Free/Traps/Platforms/Grey Off.png"/>
 </tile>
 <tile id="6" type="Spike">
  <properties>
   <property name="side" value="Bottom"/>
  </properties>
  <image width="16" height="16" source="../../Free/Traps/Spikes/idle_bottom/0.png"/>
 </tile>
 <tile id="7" type="Spike">
  <properties>
   <property name="side" value="Top"/>
  </properties>
  <image width="16" height="16" source="../../Free/Traps/Spikes/idle_top/0.png"/>
 </tile>
 <tile id="8" type="Trampoline">
  <properties>
   <property name="direction" value="Bottom"/>
  </properties>
  <image width="28" height="28" source="../../Free/Traps/Trampoline/Bottom/Idle/0.png"/>
 </tile>
 <tile id="9" type="Trampoline">
  <properties>
   <property name="direction" value="Left"/>
  </properties>
  <image width="28" height="28" source="../../Free/Traps/Trampoline/Left/Idle/0.png"/>
 </tile>
 <tile id="10" type="Trampoline">
  <properties>
   <property name="direction" value="Right"/>
  </properties>
  <image width="28" height="28" source="../../Free/Traps/Trampoline/Right/Idle/0.png"/>
 </tile>
 <tile id="11" type="Trampoline">
  <properties>
   <property name="direction" value="Top"/>
  </properties>
  <image width="28" height="28" source="../../Free/Traps/Trampoline/Top/Idle.png"/>
 </tile>
 <tile id="12" type="Checkpoint">
  <image width="64" height="64" source="../../Free/Items/Checkpoints/Checkpoint/Checkpoint (Flag Idle)(64x64)/0.png"/>
 </tile>
 <tile id="13" type="End">
  <image width="64" height="64" source="../../Free/Items/Checkpoints/End/End (IDLE) (64x64)/0.png"/>
 </tile>
 <tile id="14" type="Start">
  <properties>
   <property name="side" value="Left"/>
  </properties>
  <image width="64" height="64" source="../../Free/Items/Checkpoints/Start/Start (Idle).png"/>
 </tile>
 <tile id="19" type="Arrow">
  <properties>
   <property name="arrow_type" value="Standard"/>
   <property name="side" value="Left"/>
  </properties>
  <image width="18" height="18" source="../../Free/Traps/Arrow/Standard/Left/0.png"/>
 </tile>
 <tile id="20" type="Arrow">
  <properties>
   <property name="arrow_type" value="Standard"/>
   <property name="side" value="Bottom"/>
  </properties>
  <image width="18" height="18" source="../../Free/Traps/Arrow/Standard/Bottom/0.png"/>
 </tile>
 <tile id="21" type="Arrow">
  <properties>
   <property name="arrow_type" value="Standard"/>
   <property name="side" value="Right"/>
  </properties>
  <image width="18" height="18" source="../../Free/Traps/Arrow/Standard/Right/0.png"/>
 </tile>
 <tile id="22" type="Arrow">
  <properties>
   <property name="arrow_type" value="Standard"/>
   <property name="side" value="Top"/>
  </properties>
  <image width="18" height="18" source="../../Free/Traps/Arrow/Standard/Top/0.png"/>
 </tile>
 <tile id="23" type="Arrow">
  <properties>
   <property name="arrow_type" value="Hit"/>
   <property name="side" value="Bottom"/>
  </properties>
  <image width="18" height="18" source="../../Free/Traps/Arrow/Hit/Bottom/0.png"/>
 </tile>
 <tile id="24" type="Arrow">
  <properties>
   <property name="arrow_type" value="Hit"/>
   <property name="side" value="Left"/>
  </properties>
  <image width="18" height="18" source="../../Free/Traps/Arrow/Hit/Left/0.png"/>
 </tile>
 <tile id="25" type="Arrow">
  <properties>
   <property name="arrow_type" value="Hit"/>
   <property name="side" value="Right"/>
  </properties>
  <image width="18" height="18" source="../../Free/Traps/Arrow/Hit/Right/0.png"/>
 </tile>
 <tile id="26" type="Arrow">
  <properties>
   <property name="arrow_type" value="Hit"/>
   <property name="side" value="Top"/>
  </properties>
  <image width="18" height="18" source="../../Free/Traps/Arrow/Hit/Top/0.png"/>
 </tile>
 <tile id="27" type="Text">
  <image width="128" height="64" source="../../Free/Menu/turorial/NinjaFrog.png"/>
 </tile>
 <tile id="28" type="Text">
  <image width="87" height="16" source="../../Free/Menu/turorial/run.png"/>
 </tile>
 <tile id="29" type="Text">
  <image width="82" height="30" source="../../Free/Menu/turorial/movement.png"/>
 </tile>
 <tile id="30" type="Text">
  <image width="128" height="32" source="../../Free/Menu/turorial/jump.png"/>
 </tile>
</tileset>
