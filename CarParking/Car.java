/**
 * @author Rishabh K Iyer (ID: 103170582)
 * @version JDK 11.0.12
 * @date 15 October 2021
 * This class represents the entity "Car"
 */
public class Car
{
    private String registrationNo, ownerName;//Registration number and car owner name
    private boolean isStaffMember;//Boolean value that says if the owner is a staff member
    private long phoneNumber;//Car owner's phone number

    /**
     * Constructor for objects of the class Car
     * @param registrationNo: The registration number of the car
     * @param ownerName: The name of its owner
     * @param phoneNumber: The owner's phone number
     * @param isStaffMember: Whether the owner is a staff member
     */
    public Car(String registrationNo, String ownerName, boolean isStaffMember, long phoneNumber)
    {
        this.registrationNo= registrationNo;
        this.ownerName= ownerName;
        this.isStaffMember= isStaffMember;
        this.phoneNumber= phoneNumber;
    }
    
    /**
     * @return This method returns a boolean stating if the owner is a staff member or not
     */
    public boolean isOwnerStaffMember()
    {
        return isStaffMember;
    }
    
    /**
     * @return The registration number of the car
     */
    public String getRegistrationNo()
    {
        return registrationNo;
    }
    
    /**
     * @return The car owner's name
     */
    public String getOwnerName()
    {
        return ownerName;
    }
    
    /**
     * @return The owner's phone number
     */
    public long getOwnerPhoneNo()
    {
        return phoneNumber;
    }
}
