/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 1.3.31
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */


public class OBUnitCell extends OBGenericData {
  private long swigCPtr;

  protected OBUnitCell(long cPtr, boolean cMemoryOwn) {
    super(openbabelJNI.SWIGOBUnitCellUpcast(cPtr), cMemoryOwn);
    swigCPtr = cPtr;
  }

  protected static long getCPtr(OBUnitCell obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if(swigCPtr != 0 && swigCMemOwn) {
      swigCMemOwn = false;
      openbabelJNI.delete_OBUnitCell(swigCPtr);
    }
    swigCPtr = 0;
    super.delete();
  }

  public OBUnitCell() {
    this(openbabelJNI.new_OBUnitCell__SWIG_0(), true);
  }

  public OBUnitCell(OBUnitCell arg0) {
    this(openbabelJNI.new_OBUnitCell__SWIG_1(OBUnitCell.getCPtr(arg0), arg0), true);
  }

  public OBGenericData Clone(OBBase arg0) {
    long cPtr = openbabelJNI.OBUnitCell_Clone(swigCPtr, this, OBBase.getCPtr(arg0), arg0);
    return (cPtr == 0) ? null : new OBGenericData(cPtr, false);
  }

  public void SetData(double a, double b, double c, double alpha, double beta, double gamma) {
    openbabelJNI.OBUnitCell_SetData__SWIG_0(swigCPtr, this, a, b, c, alpha, beta, gamma);
  }

  public void SetData(vector3 v1, vector3 v2, vector3 v3) {
    openbabelJNI.OBUnitCell_SetData__SWIG_1(swigCPtr, this, vector3.getCPtr(v1), v1, vector3.getCPtr(v2), v2, vector3.getCPtr(v3), v3);
  }

  public void SetOffset(vector3 v1) {
    openbabelJNI.OBUnitCell_SetOffset(swigCPtr, this, vector3.getCPtr(v1), v1);
  }

  public void SetSpaceGroup(String sg) {
    openbabelJNI.OBUnitCell_SetSpaceGroup__SWIG_0(swigCPtr, this, sg);
  }

  public void SetSpaceGroup(int sg) {
    openbabelJNI.OBUnitCell_SetSpaceGroup__SWIG_1(swigCPtr, this, sg);
  }

  public void SetLatticeType(OBUnitCell.LatticeType lt) {
    openbabelJNI.OBUnitCell_SetLatticeType(swigCPtr, this, lt.swigValue());
  }

  public double GetA() {
    return openbabelJNI.OBUnitCell_GetA(swigCPtr, this);
  }

  public double GetB() {
    return openbabelJNI.OBUnitCell_GetB(swigCPtr, this);
  }

  public double GetC() {
    return openbabelJNI.OBUnitCell_GetC(swigCPtr, this);
  }

  public double GetAlpha() {
    return openbabelJNI.OBUnitCell_GetAlpha(swigCPtr, this);
  }

  public double GetBeta() {
    return openbabelJNI.OBUnitCell_GetBeta(swigCPtr, this);
  }

  public double GetGamma() {
    return openbabelJNI.OBUnitCell_GetGamma(swigCPtr, this);
  }

  public vector3 GetOffset() {
    return new vector3(openbabelJNI.OBUnitCell_GetOffset(swigCPtr, this), true);
  }

  public String GetSpaceGroup() {
    return openbabelJNI.OBUnitCell_GetSpaceGroup(swigCPtr, this);
  }

  public OBUnitCell.LatticeType GetLatticeType(int spacegroup) {
    return OBUnitCell.LatticeType.swigToEnum(openbabelJNI.OBUnitCell_GetLatticeType__SWIG_0(swigCPtr, this, spacegroup));
  }

  public OBUnitCell.LatticeType GetLatticeType() {
    return OBUnitCell.LatticeType.swigToEnum(openbabelJNI.OBUnitCell_GetLatticeType__SWIG_1(swigCPtr, this));
  }

  public vVector3 GetCellVectors() {
    return new vVector3(openbabelJNI.OBUnitCell_GetCellVectors(swigCPtr, this), true);
  }

  public matrix3x3 GetCellMatrix() {
    return new matrix3x3(openbabelJNI.OBUnitCell_GetCellMatrix(swigCPtr, this), true);
  }

  public matrix3x3 GetOrthoMatrix() {
    return new matrix3x3(openbabelJNI.OBUnitCell_GetOrthoMatrix(swigCPtr, this), true);
  }

  public matrix3x3 GetFractionalMatrix() {
    return new matrix3x3(openbabelJNI.OBUnitCell_GetFractionalMatrix(swigCPtr, this), true);
  }

  public int GetSpaceGroupNumber(String name) {
    return openbabelJNI.OBUnitCell_GetSpaceGroupNumber(swigCPtr, this, name);
  }

  public double GetCellVolume() {
    return openbabelJNI.OBUnitCell_GetCellVolume(swigCPtr, this);
  }

  public final static class LatticeType {
    public final static LatticeType Undefined = new LatticeType("Undefined");
    public final static LatticeType Triclinic = new LatticeType("Triclinic");
    public final static LatticeType Monoclinic = new LatticeType("Monoclinic");
    public final static LatticeType Orthorhombic = new LatticeType("Orthorhombic");
    public final static LatticeType Tetragonal = new LatticeType("Tetragonal");
    public final static LatticeType Rhombohedral = new LatticeType("Rhombohedral");
    public final static LatticeType Hexagonal = new LatticeType("Hexagonal");
    public final static LatticeType Cubic = new LatticeType("Cubic");

    public final int swigValue() {
      return swigValue;
    }

    public String toString() {
      return swigName;
    }

    public static LatticeType swigToEnum(int swigValue) {
      if (swigValue < swigValues.length && swigValue >= 0 && swigValues[swigValue].swigValue == swigValue)
        return swigValues[swigValue];
      for (int i = 0; i < swigValues.length; i++)
        if (swigValues[i].swigValue == swigValue)
          return swigValues[i];
      throw new IllegalArgumentException("No enum " + LatticeType.class + " with value " + swigValue);
    }

    private LatticeType(String swigName) {
      this.swigName = swigName;
      this.swigValue = swigNext++;
    }

    private LatticeType(String swigName, int swigValue) {
      this.swigName = swigName;
      this.swigValue = swigValue;
      swigNext = swigValue+1;
    }

    private LatticeType(String swigName, LatticeType swigEnum) {
      this.swigName = swigName;
      this.swigValue = swigEnum.swigValue;
      swigNext = this.swigValue+1;
    }

    private static LatticeType[] swigValues = { Undefined, Triclinic, Monoclinic, Orthorhombic, Tetragonal, Rhombohedral, Hexagonal, Cubic };
    private static int swigNext = 0;
    private final int swigValue;
    private final String swigName;
  }

}
