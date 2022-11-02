/**
 * @author Rishabh K Iyer (ID: 103170582)
 * @version JDK 11.0.12
 * @date 15 October 2021
 * This class represents a parking slot.
 */
public class ParkingSlot
{
    private String slotId;//The slot ID of each slot (uppercase letter followed by two digits)
    private char slotType;//Whether the slot is for staff or visitors. If it is for staff it contains S, if it is for visitors it contains V
    private Car car;//The car parked in this slot

    /**
     * Constructor for objects of class ParkingSlot
     * @param slotId: The ID of the parking slot
     * @param slotType: Indicates whether the slot is for visitors or staff members ('V' implies it is for visitors and 'S' means it is for staff members)
     * @param car: The details of the car parked in it. If it is empty, this object will have a null value.
     */
    public ParkingSlot(String slotId, char slotType, Car car)
    {
        this.slotId= slotId;
        this.slotType= slotType;
        this.car=car;
    }
    
    /**
     * @param count : The number of staff parking slots that should be generated
     * @param type : The type of the parking slots that should be generated, that is, staff or visitor (S or V)
     */
    public static void addParkingSlots(int count, char type) throws Exception
    {
        int currentChar=65, number=0;
        
        if(type == 'V')
        {
            currentChar = 66;
        }
        
        for(int ind=0;ind<count;ind++)
        {
            char letter = (char) currentChar;
            String slotId = Character.toString(letter);
            
            if(number == 0)
            {
                slotId=slotId.concat("00");
                number++;
            }
            else if(number<=99)
            {
                if(number/10==0)
                {
                    //Implies that the number has only one digit
                    String num =  "0"+number;
                    slotId=slotId.concat(num);
                }
                else
                {
                    slotId=slotId.concat(String.valueOf(number));
                }
                
                number++;
                
                if(number==100)
                {
                    number=0;
                    currentChar+=2;                    
                }
            }
            
            ParkingSlot ps = new ParkingSlot(slotId, type, null);
            CarPark.addSlot(ps);
        }
    }
    
    /**
     * @param car: The car that should be parked in this slot
     */
    public boolean addCar(Car car)  throws Exception
    {
        if(this.car==null)
        {
            //If the owner of this car does fall under the category this parking slot has been reserved for, then the car cannot be parked here.
            if((car.isOwnerStaffMember() && slotType!='S') || (!car.isOwnerStaffMember() && slotType!='V'))
            {
                return false;
            }
            else if(car.getRegistrationNo()!=null && CarPark.getSlotFromRegistrationNo(car.getRegistrationNo())!=null)
            {
                //If this if statement is true, then it means that this car is already parked in some other slot
                return false;
            }
            else
            {
                this.car= car;
                return true;
            }
        }
        else
        {
            //If this statement is true it means that this slot is already occupied
            return false;
        }
    }
    
    /**
     * This method is used to remove the car added to this slot. This is done by assigning a null value to 'car'.
     */
    public void removeCar() throws Exception
    {
        car= null;
    }
    
    /**
     * @return This method returns the slot ID
     */
    public String getSlotId() 
    {
        return slotId;
    }
    
    /**
     * @return This method returns the car parked in this slot
     */
    public Car getParkedCar() 
    {
        return car;
    }
    
    /**
     * @return This method returns the slot type: S (Staff) or V (Visitors)
     */
    public char getSlotType()
    {
        return slotType;
    }
}
