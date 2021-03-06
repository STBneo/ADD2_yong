/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 1.3.31
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */


public class OBAromaticTyper extends OBGlobalDataBase {
  private long swigCPtr;

  protected OBAromaticTyper(long cPtr, boolean cMemoryOwn) {
    super(openbabelJNI.SWIGOBAromaticTyperUpcast(cPtr), cMemoryOwn);
    swigCPtr = cPtr;
  }

  protected static long getCPtr(OBAromaticTyper obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if(swigCPtr != 0 && swigCMemOwn) {
      swigCMemOwn = false;
      openbabelJNI.delete_OBAromaticTyper(swigCPtr);
    }
    swigCPtr = 0;
    super.delete();
  }

  public OBAromaticTyper() {
    this(openbabelJNI.new_OBAromaticTyper(), true);
  }

  public long GetSize() {
    return openbabelJNI.OBAromaticTyper_GetSize(swigCPtr, this);
  }

  public void ParseLine(String arg0) {
    openbabelJNI.OBAromaticTyper_ParseLine(swigCPtr, this, arg0);
  }

  public void AssignAromaticFlags(OBMol arg0) {
    openbabelJNI.OBAromaticTyper_AssignAromaticFlags(swigCPtr, this, OBMol.getCPtr(arg0), arg0);
  }

  public void PropagatePotentialAromatic(OBAtom arg0) {
    openbabelJNI.OBAromaticTyper_PropagatePotentialAromatic(swigCPtr, this, OBAtom.getCPtr(arg0), arg0);
  }

  public void SelectRootAtoms(OBMol arg0, boolean avoidInnerRingAtoms) {
    openbabelJNI.OBAromaticTyper_SelectRootAtoms__SWIG_0(swigCPtr, this, OBMol.getCPtr(arg0), arg0, avoidInnerRingAtoms);
  }

  public void SelectRootAtoms(OBMol arg0) {
    openbabelJNI.OBAromaticTyper_SelectRootAtoms__SWIG_1(swigCPtr, this, OBMol.getCPtr(arg0), arg0);
  }

  public void ExcludeSmallRing(OBMol arg0) {
    openbabelJNI.OBAromaticTyper_ExcludeSmallRing(swigCPtr, this, OBMol.getCPtr(arg0), arg0);
  }

  public void CheckAromaticity(OBAtom root, int searchDepth) {
    openbabelJNI.OBAromaticTyper_CheckAromaticity(swigCPtr, this, OBAtom.getCPtr(root), root, searchDepth);
  }

  public boolean TraverseCycle(OBAtom root, OBAtom atom, OBBond prev, SWIGTYPE_p_std__pairTint_int_t er, int depth) {
    return openbabelJNI.OBAromaticTyper_TraverseCycle(swigCPtr, this, OBAtom.getCPtr(root), root, OBAtom.getCPtr(atom), atom, OBBond.getCPtr(prev), prev, SWIGTYPE_p_std__pairTint_int_t.getCPtr(er), depth);
  }

}
