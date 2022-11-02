import java.util.ArrayList;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

/**
 * @author Rishabh K Iyer (ID: 103170582)
 * @version JDK 11.0.12
 * @date 15 October 2021
 * This class maintains a list of all the available parking slots.
 */
public class CarPark
{
    //A list of all the available parking slots
    private static ArrayList<ParkingSlot> slots = new ArrayList<ParkingSlot>();

    /**
     * This method is used to add a slot to the list of parking slots
     * @param slot: The parking slot object that needs to be added
     */
    public static boolean addSlot(ParkingSlot slot) throws Exception
    {
        String slotId= slot.getSlotId();
        
        //Checking if the given slot ID is unique
        boolean isUnique = getSlot(slotId)==null?true:false;
        
        if(!isUnique)
        {
            return false;
        }
        else
        {            
            slots.add(slot);
        }
        return true;
    }
    
    /**
     * This method is used to delete a slot
     * @param slot: The parking slot that needs to be deleted
     */
    public static boolean deleteSlot(ParkingSlot slot) throws Exception
    {
        //Checking whether a car is parked in this slot
        if(slot.getParkedCar()!=null)
        {
            return false;
        }
        else
        {
            boolean isDeleted=false;
            
            for(int ind=0;ind<slots.size();ind++)
            {
                if(slot.getSlotId()!=null && slot.getSlotId().equals(slots.get(ind).getSlotId()))
                {
                    slots.remove(ind);
                    isDeleted=true;
                    break;
                }
            }
            
            if(isDeleted)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    }
    
    /**
     * @return This method returns the parking slot having the slot ID passed as an argument
     * @param slotId: The slot ID of the slot that we intend to fetch
     */
    public static ParkingSlot getSlot(String slotId) throws Exception
    {
        if(slotId!=null && slots!=null)
        {
            for(int ind=0;ind<slots.size();ind++)
            {
                if(slotId.equals((slots.get(ind)).getSlotId()))
                {
                    return slots.get(ind);
                }
            }
        }
        return null;
    }
    
    /**
     * This method prints all the slots available in the parking lot
     */
    public static void getParkingSlots()
    {
        JFrame jframe= new JFrame("Parking Slots");
        
        try
        {             
            JPanel panel =new JPanel();
            
            if(slots!=null && slots.size()>0)
            {                
                for(int ind=0;ind<slots.size();ind++)
                {
                    ParkingSlot slot = slots.get(ind);
                    String slotId = slot.getSlotId();
                    String slotType = (slot.getSlotType()=='S'?"Staff Parking":"Visitor Parking");
                    String carStr="";  
                    
                    if(slot.getParkedCar()==null)
                    {
                       carStr="There is no car in this slot.";
                    }
                    else
                    {                       
                       Car car = slot.getParkedCar();
                       carStr="The car parked in this slot has registration number "+car.getRegistrationNo()+".<br> Its owner is "+car.getOwnerName()+".<br>The owner's phone number is "+car.getOwnerPhoneNo()+".";
                    }
                    
                    JLabel label = new JLabel("<html>Slot ID: "+slotId+"<br>Slot Type: "+slotType+"<br>"+carStr+"</html>");
                    label.setFont(new Font(label.getFont().getName(),label.getFont().getStyle(),15)); 
                    
                    if(slot.getParkedCar()==null)
                    {
                       if("Staff Parking".equals(slotType))
                       {
                            label.setBackground(Color.CYAN);
                       }
                       else
                       {
                            label.setBackground(Color.YELLOW);
                       }
                       label.setSize(new Dimension(500, 180));
                    }
                    else
                    {
                       if("Staff Parking".equals(slotType))
                       {
                            label.setBackground(Color.GREEN);
                       }
                       else
                       {
                            label.setBackground(Color.ORANGE);
                       } 
                       label.setSize(new Dimension(500, 320));
                    }
                    
                    label.setOpaque(true);
                    panel.add(label);
                }
                
                int rows = slots.size()/2;
                
                panel.setLayout(new GridLayout(rows+1,2,10,10));
                JScrollPane slotsPane = new JScrollPane(panel);  
  
                slotsPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);  
                slotsPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS); 
                
                jframe.getContentPane().add(slotsPane);
            }
            else
            {
                JLabel label = new JLabel("There are no parking slots as of now.");
                label.setFont(new Font(label.getFont().getName(),label.getFont().getStyle(),20));
                label.setHorizontalAlignment(SwingConstants.CENTER);
                label.setVerticalAlignment(SwingConstants.CENTER);
                    
                panel.add(label);
                jframe.getContentPane().add(panel);
            }
            
            jframe.setSize(1100,800);
            jframe.setVisible(true);
        } catch(Exception ex)
        {
            //Unexpected error occurred
            jframe.dispose();
        }
    }
    
    /**
     * @return The entire list of parking slots
     */
    public static ArrayList<ParkingSlot> getParkingSlotsList() throws Exception
    {
        return slots;
    }
    
    /**
     * @param regNo: The registration number of the car that the user wants to find
     * @return The parking slot in which this car is present
     */
    public static ParkingSlot getSlotFromRegistrationNo(String regNo) throws Exception
    {
        ArrayList<ParkingSlot> slotsArray = getParkingSlotsList();
        
        for(int ind=0;ind<slotsArray.size();ind++)
        {
            ParkingSlot pSlot= slotsArray.get(ind);
            String reg_no= pSlot.getParkedCar()!=null?pSlot.getParkedCar().getRegistrationNo():null;
                            
            if(reg_no != null && reg_no.equals(regNo))
            {
                return pSlot;
            }
        }
        return null;
    }
}
